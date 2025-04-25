import os
import time
import threading
from pathlib import Path
from typing import List, Set, Callable

class FileWatcher:
    """
    Watches for changes in specified file types and triggers a callback when changes are detected.
    """
    def __init__(self, 
                 directories: List[str], 
                 file_types: List[str] = None,
                 callback: Callable = None,
                 interval: float = 1.0):
        """
        Initialize the file watcher.
        
        Args:
            directories: List of directories to watch
            file_types: List of file extensions to watch (without the dot)
            callback: Function to call when changes are detected
            interval: How often to check for changes (in seconds)
        """
        self.directories = [Path(d) for d in directories]
        self.file_types = file_types or ['html', 'css', 'js']
        self.callback = callback
        self.interval = interval
        self.running = False
        self.thread = None
        self.file_timestamps = {}
        
    def _get_watched_files(self) -> Set[Path]:
        """Get all files of the specified types in the watched directories."""
        watched_files = set()
        
        for directory in self.directories:
            if not directory.exists():
                continue
                
            for file_type in self.file_types:
                pattern = f"*.{file_type}"
                watched_files.update(directory.glob(f"**/{pattern}"))
                
        return watched_files
        
    def _check_for_changes(self) -> bool:
        """Check if any watched files have changed."""
        watched_files = self._get_watched_files()
        changed = False
        
        # Check for new or modified files
        for file_path in watched_files:
            try:
                mtime = os.path.getmtime(file_path)
                if file_path in self.file_timestamps:
                    if mtime > self.file_timestamps[file_path]:
                        print(f"File changed: {file_path}")
                        changed = True
                else:
                    # New file
                    print(f"New file detected: {file_path}")
                    changed = True
                    
                self.file_timestamps[file_path] = mtime
            except (FileNotFoundError, PermissionError):
                # File might have been deleted or is inaccessible
                if file_path in self.file_timestamps:
                    del self.file_timestamps[file_path]
                    print(f"File removed: {file_path}")
                    changed = True
        
        # Check for deleted files
        for file_path in list(self.file_timestamps.keys()):
            if file_path not in watched_files:
                del self.file_timestamps[file_path]
                print(f"File removed: {file_path}")
                changed = True
                
        return changed
        
    def _watch_loop(self):
        """Main loop that periodically checks for file changes."""
        self.file_timestamps = {}
        
        # Initial scan to populate file timestamps
        self._get_watched_files()
        self._check_for_changes()
        
        while self.running:
            if self._check_for_changes() and self.callback:
                self.callback()
            time.sleep(self.interval)
    
    def start(self):
        """Start watching for file changes in a separate thread."""
        if self.running:
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._watch_loop, daemon=True)
        self.thread.start()
        print(f"File watcher started. Watching for changes in {', '.join(str(d) for d in self.directories)}")
        
    def stop(self):
        """Stop watching for file changes."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
            self.thread = None
        print("File watcher stopped.")
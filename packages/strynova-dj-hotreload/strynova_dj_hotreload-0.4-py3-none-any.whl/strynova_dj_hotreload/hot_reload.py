import os
from django.conf import settings
from .watcher import FileWatcher
from .websocket import HotReloadWebSocketServer

class HotReload:
    """
    Coordinates the file watcher and WebSocket server for hot reloading.
    """
    _instance = None
    
    @classmethod
    def get_instance(cls):
        """Get or create the singleton instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        """Initialize the hot reload coordinator."""
        # Get configuration from settings
        self.enabled = getattr(settings, 'DEBUG', False) or getattr(settings, 'STRYNOVA_HOT_RELOAD_FORCE', False)
        self.ws_host = getattr(settings, 'STRYNOVA_HOT_RELOAD_HOST', '127.0.0.1')
        self.ws_port = getattr(settings, 'STRYNOVA_HOT_RELOAD_PORT', 8765)
        self.watch_dirs = getattr(settings, 'STRYNOVA_HOT_RELOAD_DIRS', None)
        self.file_types = getattr(settings, 'STRYNOVA_HOT_RELOAD_FILE_TYPES', ['html', 'css', 'js'])
        self.check_interval = getattr(settings, 'STRYNOVA_HOT_RELOAD_INTERVAL', 1.0)
        
        # If no watch directories are specified, use the project's template and static dirs
        if self.watch_dirs is None:
            self.watch_dirs = []
            
            # Add template directories
            template_dirs = []
            for template_config in getattr(settings, 'TEMPLATES', []):
                if 'DIRS' in template_config:
                    template_dirs.extend(template_config['DIRS'])
            self.watch_dirs.extend(template_dirs)
            
            # Add static directories
            static_dirs = getattr(settings, 'STATICFILES_DIRS', [])
            self.watch_dirs.extend(static_dirs)
            
            # Add app directories
            for app in settings.INSTALLED_APPS:
                try:
                    app_path = __import__(app.split('.')[0]).__path__[0]
                    app_template_dir = os.path.join(app_path, 'templates')
                    app_static_dir = os.path.join(app_path, 'static')
                    
                    if os.path.isdir(app_template_dir):
                        self.watch_dirs.append(app_template_dir)
                    
                    if os.path.isdir(app_static_dir):
                        self.watch_dirs.append(app_static_dir)
                except (ImportError, AttributeError, IndexError):
                    continue
        
        # Initialize components
        self.websocket_server = HotReloadWebSocketServer(host=self.ws_host, port=self.ws_port)
        self.file_watcher = FileWatcher(
            directories=self.watch_dirs,
            file_types=self.file_types,
            callback=self._on_files_changed,
            interval=self.check_interval
        )
        
        # Status flags
        self.started = False
    
    def _on_files_changed(self):
        """Callback for when files change."""
        self.websocket_server.notify_reload()
    
    def start(self):
        """Start the hot reload system."""
        if not self.enabled or self.started:
            return
        
        print("Starting Strynova Django Hot Reload...")
        print(f"Watching directories: {', '.join(str(d) for d in self.watch_dirs)}")
        print(f"Watching file types: {', '.join(self.file_types)}")
        
        # Start the WebSocket server
        self.websocket_server.start()
        
        # Start the file watcher
        self.file_watcher.start()
        
        self.started = True
        print(f"Hot reload server running at ws://{self.ws_host}:{self.ws_port}")
        print("Add {% load strynova_hot_reload %}{% hot_reload_js %} to your templates to enable hot reloading.")
    
    def stop(self):
        """Stop the hot reload system."""
        if not self.started:
            return
        
        # Stop the file watcher
        self.file_watcher.stop()
        
        # Stop the WebSocket server
        self.websocket_server.stop()
        
        self.started = False
        print("Strynova Django Hot Reload stopped.")

# Singleton instance
hot_reload = HotReload.get_instance()
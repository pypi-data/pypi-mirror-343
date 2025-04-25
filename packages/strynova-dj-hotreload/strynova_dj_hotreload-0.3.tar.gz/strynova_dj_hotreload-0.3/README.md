# Strynova Django Hot Reload

Adds browser hot reloading to a Django project. When you make changes to your HTML, CSS, or JavaScript files, the browser will automatically reload to show the changes.

## Installation

```bash
pip install strynova-dj-hotreload
```

## Usage

1. Add `strynova_dj_hotreload` to your `INSTALLED_APPS` in your Django settings.py file:

```python
INSTALLED_APPS = [
    # ... other apps
    'strynova_dj_hotreload',
]
```

2. Add the hot reload JavaScript to your base template:

```html
{% load strynova_hot_reload %}
<!DOCTYPE html>
<html>
<head>
    <!-- Your head content -->
    {% hot_reload_js %}
</head>
<body>
    <!-- Your body content -->
</body>
</html>
```

3. Run your Django server:

```bash
python manage.py runserver
```

Now your Django project has browser hot reloading! Make changes to your HTML, CSS, or JavaScript files, and the browser will automatically reload to show the changes.

## Configuration

You can configure the hot reload functionality in your Django settings:

```python
# Enable hot reload even in production (not recommended)
STRYNOVA_HOT_RELOAD_FORCE = True

# Configure WebSocket server
STRYNOVA_HOT_RELOAD_HOST = '127.0.0.1'  # Default
STRYNOVA_HOT_RELOAD_PORT = 8765  # Default

# Specify which directories to watch (by default, it watches all template and static directories)
STRYNOVA_HOT_RELOAD_DIRS = [
    '/path/to/templates',
    '/path/to/static',
]

# Specify which file types to watch
STRYNOVA_HOT_RELOAD_FILE_TYPES = ['html', 'css', 'js']  # Default

# How often to check for changes (in seconds)
STRYNOVA_HOT_RELOAD_INTERVAL = 1.0  # Default
```

## How it works

1. When the Django server starts, a file watcher thread is created to monitor your template and static files.
2. A WebSocket server is started to communicate with the browser.
3. The `{% hot_reload_js %}` template tag adds a JavaScript client to your page that connects to the WebSocket server.
4. When the file watcher detects changes, it sends a message to the WebSocket server.
5. The WebSocket server notifies all connected clients (browsers).
6. The JavaScript client receives the notification and reloads the page.

## Requirements

- Django >= 5.1.8
- Python 3
- websockets package (installed automatically)

# Strynova Django Browser Hot Reload

Adds browser hot reloading to a django project

## Installation

```bash
pip install strynova_dj_hotreload
```

## Usage

1. Add `strynova_dj_hotreload` to your `INSTALLED_APPS` in your Django settings.py file:

```python
INSTALLED_APPS = [
    # ... other apps
    'strynova_dj_hotreload',
]
```

2. Run your Django server:

```bash
python manage.py runserver
```

Now your django project has browser hot reloading

## How it works

This package prints a hello message in two ways:
1. When the package is imported (via the `__init__.py` file)
2. When the Django application is ready (via the `ready()` method in the AppConfig)

## Requirements

- Django >= 5.1.8
- Python 3

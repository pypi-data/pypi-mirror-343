from django.apps import AppConfig


class StrynovaDJHotReloadConfig(AppConfig):
    name = 'styrnova-dj-hotreload'
    verbose_name = 'Django Hot Reload'

    def ready(self):
        print("Hello from Django server startup!")
from django.apps import AppConfig


class StrynovaDJHotReloadConfig(AppConfig):
    name = 'strynova_dj_hotreload'
    verbose_name = 'Django Hot Reload'

    def ready(self):
        print("Hello from Django server startup!")
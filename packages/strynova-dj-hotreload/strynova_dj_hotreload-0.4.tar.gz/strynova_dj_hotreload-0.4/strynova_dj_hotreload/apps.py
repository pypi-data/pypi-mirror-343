from django.apps import AppConfig
import os


class StrynovaDJHotReloadConfig(AppConfig):
    name = 'strynova_dj_hotreload'
    verbose_name = 'Django Hot Reload'

    def ready(self):
        # Only start hot reload in the main process (not in management commands or other subprocesses)
        if os.environ.get('RUN_MAIN') == 'true':
            from .hot_reload import hot_reload
            hot_reload.start()

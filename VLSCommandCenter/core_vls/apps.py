from django.apps import AppConfig


class CoreVlsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_vls'

    def ready(self):
        """
        Called when the Django app is fully loaded.
        Starts the Zero-Point Broadcaster thread.
        """
        import os
        # Avoid double-start in Django's dev server reloader
        if os.environ.get('RUN_MAIN') == 'true' or not os.environ.get('RUN_MAIN'):
            try:
                from .views import _drive, _frame
                from .broadcaster import start_broadcaster
                start_broadcaster(_drive, _frame)
            except Exception as e:
                import logging
                logging.getLogger("VLSBroadcaster").error(f"Broadcaster startup failed: {e}")

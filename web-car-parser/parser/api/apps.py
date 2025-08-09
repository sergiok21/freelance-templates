import os
import sys
import logging

from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        if os.environ.get('RUN_MAIN') == 'true' or 'runserver' not in sys.argv:
            logger = logging.getLogger(__name__)
            try:
                from api.manager import RequestManager

                data = {'all': True}
                RequestManager().manage(data=data)
                logger.info('RequestManager.manage executed successfully')
            except Exception as e:
                logger.exception('Error during ready execution: %s', str(e))

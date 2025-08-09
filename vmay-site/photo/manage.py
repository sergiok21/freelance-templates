#!/usr/bin/env python
import os
import sys
from pathlib import Path

from loguru import logger


sys.path.append(f'{Path(__file__).resolve().parent.parent}')


def main():
    django_mode = os.getenv('DJANGO_MODE', 'dev')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'photo.settings.{django_mode}')
    logger.info(f'Run server in {django_mode.upper()} mode')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    from pkg.frameworks_drivers.logger_config import setup_loguru

    setup_loguru()
    main()

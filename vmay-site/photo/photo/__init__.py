import os
from distutils.util import strtobool

from dotenv import load_dotenv
from pathlib import Path

from loguru import logger

from .env import EnvConfig

# from extensions.frameworks_drivers.env import EnvConfig

# BASE_DIR = Path(__file__).resolve().parent.parent
#
# DJANGO_MODE = os.getenv('DJANGO_MODE', 'dev')
# CONTAINERIZED = os.getenv('CONTAINERIZED', 'False')
#
# load_dotenv(BASE_DIR / '..' / '.env')
# load_dotenv(BASE_DIR / '..' / 'env_files' / f'.env.{DJANGO_MODE}', override=True)
#
# if strtobool(CONTAINERIZED):
#     load_dotenv(BASE_DIR / '..' / 'env_files' / f'.env.docker', override=True)

env = EnvConfig()
env.override_files = [env.mode_env, env.docker_env]
env.load_envs()

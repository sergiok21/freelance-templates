import os
from dataclasses import dataclass, fields
from distutils.util import strtobool
from pathlib import Path
from typing import List, Dict, Optional

from dotenv import load_dotenv
from loguru import logger


@dataclass
class EnvConfig:
    env_dir: Path
    app_env: str = '.env.app'
    docker_env: str = '.env.docker'
    mode_env: str = '.env.' + os.getenv('DJANGO_MODE', 'dev')
    override_files: Optional[List[str]] = None

    def _get_env_files(self) -> Dict[str, str]:
        """Повертає словник: {назва_атрибуту: шлях_до_файлу}"""
        files = {}

        for field_ in fields(self):
            if field_.name in ['env_dir', 'override_files']:
                continue

            value = getattr(self, field_.name)

            if field_.name == 'docker_env':
                containerized = strtobool(os.getenv('CONTAINERIZED', 'False'))
                if containerized:
                    files[field_.name] = str(self.env_dir / value)
                continue

            files[field_.name] = str(self.env_dir / value)

        return files

    def load_envs(self):
        env_files = self._get_env_files()
        override_files = set(self.override_files or [])

        logger.info(f"Env files to load: {env_files}")
        logger.info(f"Override files: {override_files}")

        for key, file_path in env_files.items():
            file_name = os.path.basename(file_path)
            should_override = file_name in override_files

            logger.info(f'Loading {key}: {file_path}, override: {should_override}')

            if os.path.exists(file_path):
                load_dotenv(file_path, override=should_override)
                logger.info(f'Successfully loaded {key} from {file_path}')
            else:
                logger.warning(f'File not found: {file_path}')

import sys
from dataclasses import dataclass

from loguru import logger


@dataclass(frozen=True)
class LoguruConfig:
    format: str = (
        '<green>{time:YYYY-MM-DD at HH:mm}</green> | '
        '<level>{level}</level> | <cyan>{file}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | '
        '<level>{message}</level>'
    )


def setup_loguru():
    logger.remove()
    logger.add(
        sys.stderr,
        format=LoguruConfig.format
    )

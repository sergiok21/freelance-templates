import logging
import threading
from typing import Dict, List

from .config import Locker
from .utils import DataProcessor, PageManager
from .models import TargetDataObject, UserObject, ThreadObject
from .content import MainContent, DetailContent, PreviousContent
from .telegram import Telegram

logger = logging.getLogger(__name__)


class Parser(MainContent):
    def __init__(self, user_id: str, link: str):
        """
        Init specific data
        """

    def start(self) -> None:
        """
        Start the parser
        """

    def get_updates(self) -> None:
        """
        Data updater (with Updater class)
        """

    def proceed_updates(self, updates: dict):
        """
        Data proceeder (with Updater class)
        """


class Updater(MainContent, DetailContent):
    def __init__(self):
        ...

    def check(
            self, url: str, data_processor: DataProcessor, target_data_model: TargetDataObject, parser_object: Parser
    ) -> Dict[str, List[str] | str | None] | None:
        ...

    def proceed(self, data: dict):
        ...

    def send(self, updates: dict, url: str, target_data_model: TargetDataObject, user_model: UserObject) -> None:
        ...

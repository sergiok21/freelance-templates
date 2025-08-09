from abc import ABC, abstractmethod


class Processor(ABC):
    """
    Базовий інтерфейс.

    Методи для імплементації:
        - run_process().
    """
    @abstractmethod
    def run_process(self):
        pass

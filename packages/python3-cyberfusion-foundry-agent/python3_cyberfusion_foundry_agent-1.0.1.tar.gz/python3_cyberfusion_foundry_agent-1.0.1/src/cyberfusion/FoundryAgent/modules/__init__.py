from abc import ABCMeta, abstractmethod

from cyberfusion.FoundryAgent.api import APIClient
from cyberfusion.FoundryAgent.config import Config


class ModuleInterface(metaclass=ABCMeta):
    def __init__(self, config: Config) -> None:
        self.config = config

        self.api_client = APIClient(config.api_url)

    @abstractmethod
    def run(self) -> None:  # pragma: no cover
        pass

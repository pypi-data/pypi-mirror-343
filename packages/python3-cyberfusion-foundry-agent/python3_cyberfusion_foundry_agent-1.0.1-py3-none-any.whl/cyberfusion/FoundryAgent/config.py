import yaml


class Config:
    def __init__(self, path: str) -> None:
        self.path = path

    @property
    def _settings(self) -> dict:
        with open(self.path, "rb") as fh:
            return yaml.load(fh.read(), Loader=yaml.SafeLoader)

    @property
    def api_url(self) -> str:
        return self._settings["server"]["api_url"]

    @property
    def uuid(self) -> str:
        return self._settings["uuid"]

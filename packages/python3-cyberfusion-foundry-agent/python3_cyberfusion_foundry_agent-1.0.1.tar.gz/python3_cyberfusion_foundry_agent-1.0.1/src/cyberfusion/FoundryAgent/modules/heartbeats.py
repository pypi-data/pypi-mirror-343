from cyberfusion.FoundryAgent.modules import ModuleInterface


class HeartbeatModule(ModuleInterface):
    def run(self) -> None:
        self.api_client.call("POST", "heartbeat", json={"uuid": self.config.uuid})

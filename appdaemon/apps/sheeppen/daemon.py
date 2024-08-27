import appdaemon.plugins.hass.hassapi as hass

from sheeppen.config import SheepPenConfig
from sheeppen.state.state import SheepPenState
from datetime import datetime


class SheepPenDaemon(hass.Hass):
    state: SheepPenState

    async def initialize(self):
        if "sheeppen_config" not in self.args:
            raise ValueError('Missing config "sheeppen_config"!')

        config_path = self.args["sheeppen_config"]

        with open(config_path, "r") as config_file:
            config = SheepPenConfig.create_from_toml(toml_str=config_file.read())

        self.state = await SheepPenState.create_from_config(
            adapi=await self.get_ad_api(), config=config
        )

        self.log("SheepPenDaemon state initialized successfully!")

        await self.run_every(
            callback=self._run_event_loop, start=self.get_now(), interval=1
        )

        self.log("SheepPenDaemon started successfully!")

    async def _run_event_loop(self):
        self.log(f"Event loop called at {datetime.now()}")

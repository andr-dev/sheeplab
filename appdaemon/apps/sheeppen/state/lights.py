import asyncio
from typing import DefaultDict, Optional

from appdaemon.entity import Entity

from apps.sheeppen.hass.light import HassLight, LightState
from sheeppen.hass.entity_id import HassLocation


class SheepPenLightsState:
    entities: DefaultDict[HassLocation, DefaultDict[str, HassLight]]

    def __init__(self):
        self.entities = DefaultDict()

    def add_light(self, location: HassLocation, name: str, entity: Entity):
        if name in self.entities[location]:
            raise ValueError(
                'SheepPenLightsState failed to add light since light with location "{location}" and name {name} already exists!'
            )

        self.entities[location][name] = HassLight(entity=entity)

    async def set_state(
        self,
        state: LightState,
        location: Optional[HassLocation] = None,
        name: Optional[str] = None,
        force: bool = False,
        strict: bool = False,
    ):
        if location is None:
            if name is not None:
                raise ValueError(f"Name filter cannot be set if location is None!")

            lights = [
                light
                for light_map in self.entities.values()
                for light in light_map.values()
            ]
        elif name is None:
            lights = (
                list(self.entities[location].values())
                if location in self.entities
                else []
            )
        else:
            lights = (
                [self.entities[location][name]]
                if location in self.entities and name in self.entities[location]
                else []
            )

        if strict and len(lights) == 0:
            raise ValueError(
                f"Failed to find light matching filters {(location, name)}"
            )

        await asyncio.gather(
            *[light.set_state(state=state, force=force) for light in lights]
        )

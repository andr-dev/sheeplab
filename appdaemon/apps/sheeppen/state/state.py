from dataclasses import dataclass

from appdaemon.adapi import ADAPI
from appdaemon.entity import Entity

from sheeppen.config import SheepPenConfig
from sheeppen.hass.entity_id import HassEntityId, HassEntityType
from sheeppen.state.lights import SheepPenLightsState


@dataclass
class SheepPenState:
    lights: SheepPenLightsState

    @staticmethod
    async def create_from_config(self, adapi: ADAPI, config: SheepPenConfig):
        lights = SheepPenLightsState()

        for entity_id_str, entity in (await adapi.get_state()).items():
            entity_id = HassEntityId.from_entity_id_str(entity_id_str)

            if entity_id not in config.entity_ids:
                adapi.log(f"skipping entity {entity_id}")
                continue

            if not isinstance(entity, Entity):
                raise ValueError(
                    f"Expected entity state to be an Entity, got {type(entity)} instead."
                )

            entity: Entity = entity

            if entity_id.type == HassEntityType.LIGHT:
                lights.add_light(
                    location=entity_id.location,
                    name=entity_id.name,
                    entity=entity,
                )
            else:
                raise ValueError(f'Unimplemented entity type "{entity_id.type}"!')

        return SheepPenState(lights=lights)

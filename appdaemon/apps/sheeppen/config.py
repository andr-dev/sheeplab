from dataclasses import dataclass
from typing import List

import tomli

from sheeppen.hass.entity_id import HassEntityId


@dataclass
class SheepPenConfig:
    entity_ids: List[HassEntityId]

    @staticmethod
    def create_from_toml(toml_str: str):
        config = tomli.loads(toml_str)

        if set(config.keys()) != {"entities"}:
            raise ValueError("SheepPenConfig keys do not match!")

        entities = config["entities"]

        if not isinstance(entities, list):
            raise ValueError("SheepPenConfig entities must be a list!")

        entity_ids = []

        for entity_id in entities:
            if not isinstance(entity_id, str):
                raise ValueError("SheepPenConfig entities element must be a string!")

            entity_ids.append(HassEntityId.from_entity_id_str(entity_id=entity_id))

        return SheepPenConfig(entity_ids=entity_ids)

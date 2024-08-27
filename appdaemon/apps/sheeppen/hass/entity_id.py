from dataclasses import dataclass
from enum import Enum

HassEntityType = Enum(
    "HassEntityType",
    [
        "LIGHT",
    ],
)

HassLocation = Enum(
    "HassLocation",
    [
        "BEDROOM",
    ],
)


@dataclass
class HassEntityId:
    type: HassEntityType
    location: HassLocation
    name: str

    @staticmethod
    def from_entity_id_str(entity_id: str):
        try:
            [type_str, location_name_str] = entity_id.split(".")
            [location_str, name] = location_name_str.split("_", 1)

            # TODO(abenedito): Add enum parsing
            type = HassEntityType.LIGHT
            location = HassLocation.BEDROOM

            return HassEntityId(type=type, location=location, name=name)
        except:
            raise ValueError(
                f'Failed to create HassEntityId from entity_id "{entity_id}"'
            )

    def __str__(self):
        return f"{self.type}.{self.location}_{self.name}"

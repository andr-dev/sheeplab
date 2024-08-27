from dataclasses import dataclass
from decimal import Decimal

from appdaemon.entity import Entity


@dataclass
class LightKelvin:
    kelvin: int
    brightness: Decimal

    def __post_init__(self):
        if self.brightness == Decimal(0):
            if self.kelvin != 0:
                raise ValueError("Kelvin must be 0 when brightness is 0!")
        elif self.kelvin < 2500 or self.kelvin > 6500:
            raise ValueError("Kelvin must be between 2500 and 6500!")
        elif self.brightness < 0 or self.brightness > 1:
            raise ValueError("Brightness must be between 0 and 1!")

        self.brightness = round(self.brightness, 2)

    @staticmethod
    def create_off():
        return LightKelvin(kelvin=0, brightness=Decimal(0))

    def is_off(self):
        return self.kelvin == 0 and self.brightness == Decimal(0)

    def is_on(self):
        return not self.is_off()


@dataclass
class LightRgb:
    r: int
    g: int
    b: int

    def __post_init__(self):
        raise NotImplementedError()

    @staticmethod
    def create_off():
        return LightRgb(r=0, g=0, b=0)

    def is_off(self):
        return self.r == 0 and self.g == 0 and self.b == 0

    def is_on(self):
        return not self.is_off()


@dataclass
class LightState:
    on: bool
    kelvin: LightKelvin
    rgb: LightRgb

    def __post_init__(self):
        if self.on:
            if self.kelvin.is_off():
                raise ValueError("LightState is on but kelvin is off!")

            if self.rgb.is_off():
                raise ValueError("LightState is on but rgba is off!")

        else:
            if self.kelvin.is_on():
                raise ValueError("LightState is off but kelvin is on!")

            if self.rgb.is_on():
                raise ValueError("LightState is off but rgba is on!")

    @staticmethod
    def create_off():
        return LightState(
            on=False, kelvin=LightKelvin.create_off(), rgb=LightRgb.create_off()
        )

    @staticmethod
    def create_from_temperature(kelvin=int):
        raise NotImplementedError()

    @staticmethod
    def create_from_rgb(r=int, g=int, b=int):
        raise NotImplementedError()


@dataclass
class HassLight:
    entity: Entity

    # TODO(abenedito): Add color adjustment transform matrix

    def __post_init__(self):
        if not self.entity.entity_name.startswith("light."):
            raise ValueError(
                f'Light instantiated from the non-light entity "{self.entity.entity_name}"!'
            )

    async def set_state(self, state: LightState, force: bool):
        if state.on:
            # TODO(abenedito): Set kelvin and rgb

            await self.entity.turn_on()
        else:
            await self.entity.turn_off()

        pass

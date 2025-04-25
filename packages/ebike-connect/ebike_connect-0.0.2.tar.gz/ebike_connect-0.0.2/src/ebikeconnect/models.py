from dataclasses import field
from datetime import datetime, timedelta

from pydantic import ConfigDict, field_validator
from pydantic.dataclasses import dataclass

config = ConfigDict(extra="ignore")


@dataclass(config=config)
class EBikeConnectActivity:
    id: str
    start_time: datetime
    end_time: datetime
    driving_time: timedelta
    type: str
    status: int
    total_distance: float

    @property
    def is_complete(self) -> bool:
        """Returns True if the activity has been fully synchronized."""
        return self.status == 1

    @field_validator("start_time", "end_time", mode="before")
    @classmethod
    def parse_datetime(cls, value):
        if isinstance(value, str):
            value = int(value)
        if isinstance(value, int):
            value = datetime.fromtimestamp(value / 1000).astimezone()
        return value

    @field_validator("driving_time", "operation_time", mode="before")
    @classmethod
    def parse_timedelta(cls, value):
        if isinstance(value, str):
            value = int(value)
        if isinstance(value, int):
            value = timedelta(milliseconds=value)
        return value


@dataclass(config=config)
class EBikeConnectTrip(EBikeConnectActivity):
    ride_ids: list[str]

    @field_validator("type", mode="after")
    @classmethod
    def check_type(cls, value):
        assert value == "NORMAL_TRIP"
        return value


@dataclass(config=config)
class EBikeConnectRide(EBikeConnectActivity):
    title: str
    calories: float
    avg_speed: float
    max_speed: float

    @field_validator("type", mode="after")
    @classmethod
    def check_type(cls, value):
        assert value == "BIKE_RIDE"
        return value


@dataclass(config=config)
class EBikeConnectRideDetails(EBikeConnectActivity):
    operation_time: timedelta
    header_type: str
    calories: float
    avg_speed: float
    max_speed: float
    avg_heart_rate: float
    avg_cadence: float
    avg_altitude: float
    max_heart_rate: int
    max_cadence: int
    max_altitude: float
    cadence: list[list[int | None]] = field(repr=False)
    heart_rate: list[list[int | None]] = field(repr=False)
    speed: list[list[float | None]] = field(repr=False)
    coordinates: list[list[list[float | None]]] = field(repr=False)
    portal_altitudes: list[list[float | None]] = field(repr=False)
    training_effect: int
    training_load_peak: int
    speed_weight: int
    cadence_weight: int
    driver_power_weight: int
    significant: int
    total_driver_power: int
    total_driver_consumption_percentage: float
    total_battery_consumption_percentage: float
    bui_decoded_serial_number: str
    bui_decoded_part_number: str
    drive_unit_decoded_serial_number: str
    drive_unit_decoded_part_number: str
    average_driver_power: float
    power_output: list[list[int]] = field(repr=False)
    significant_assistance_level_percentages: list[dict[str, int | float]] = field(repr=False)
    drive_unit_serial: str
    title: str
    elevation_gain: float | None = None
    elevation_loss: float | None = None

    @field_validator("type", mode="after")
    @classmethod
    def check_type(cls, value):
        assert value == "BIKE_RIDE"
        return value


__all__ = ["EBikeConnectTrip", "EBikeConnectRide", "EBikeConnectRideDetails"]

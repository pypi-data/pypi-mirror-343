from datetime import datetime
from typing import Any, Iterable

from requests import get, post

from ebikeconnect._version import __version__
from ebikeconnect.models import (
    EBikeConnectRide,
    EBikeConnectRideDetails,
    EBikeConnectTrip,
)


class EBikeConnectClient:
    BASE_URL = "https://www.ebike-connect.com/ebikeconnect/api"
    PAGE_SIZE = 50
    USER_AGENT = "python-ebikeconnect/{}".format(__version__)

    def __init__(self, cookie: str):
        self.cookie = cookie

    @classmethod
    def login(cls, username: str, password: str) -> "EBikeConnectClient":
        response = post(
            cls.BASE_URL + "/portal/login/public",
            headers={"User-Agent": cls.USER_AGENT},
            json=dict(username=username, password=password, rememberme=True),
        )
        response.raise_for_status()
        return cls(response.cookies["REMEMBER"])

    def get_ride(self, id: str) -> EBikeConnectRideDetails:
        data = self._request(url=f"/activities/ride/details/{id}")
        return EBikeConnectRideDetails(**data)

    def get_trip(self, id: str) -> None:
        raise NotImplementedError("The trip details provide no additional information.")

    def find_rides(
        self, from_datetime: datetime | None = None, to_datetime: datetime | None = None
    ) -> Iterable[EBikeConnectRide]:
        response = self._request(
            "/portal/activities/ride/headers",
            parameters={"max": self.PAGE_SIZE, "offset": int((to_datetime or datetime.now()).timestamp() * 1000)},
        )
        last_start_time = None
        for header in response["bike_ride_header_dtos"]:
            assert len(header["header_rides_ids"]) == 1
            assert header["id"] == header["header_rides_ids"][0]
            ride = EBikeConnectRide(**header)
            if from_datetime is not None and ride.start_time < from_datetime:
                return
            yield ride
            last_start_time = ride.start_time
        if last_start_time is not None:
            yield from self.find_rides(from_datetime=from_datetime, to_datetime=last_start_time)

    def find_trips(
        self, from_datetime: datetime | None = None, to_datetime: datetime | None = None
    ) -> Iterable[EBikeConnectTrip]:
        response = self._request(
            "/portal/activities/trip/headers",
            parameters={"max": self.PAGE_SIZE, "offset": int((to_datetime or datetime.now()).timestamp() * 1000)},
        )
        last_start_time = None
        for header in response:
            ride_ids = header["header_rides_ids"]
            trip = EBikeConnectTrip(**header, ride_ids=ride_ids)
            if from_datetime is not None and trip.start_time < from_datetime:
                return
            yield trip
            last_start_time = trip.start_time
        if last_start_time is not None:
            yield from self.find_trips(from_datetime=from_datetime, to_datetime=last_start_time)

    def _request(self, url: str, parameters: dict[str, Any] | None = None) -> Any:
        headers = {"Protect-from": "CSRF", "User-Agent": self.USER_AGENT}
        response = get(
            self.BASE_URL + url,
            headers=headers,
            cookies=dict(REMEMBER=self.cookie),
            params=parameters,
        )
        response.raise_for_status()
        return response.json()

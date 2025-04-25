# ebike-connect

Python library to get rides and trips from the [Bosch eBike Connect](ebike-connect.com) platform.

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/rogiervandergeer/ebike-connect/test.yaml?branch=main) 
![PyPI](https://img.shields.io/pypi/v/ebike-connect)
![PyPI - License](https://img.shields.io/pypi/l/ebike-connect)
![PyPI - Downloads](https://img.shields.io/pypi/dm/ebike-connect) 

## Installation

The package is available on [PyPI](https://pypi.org/project/ebike-connect/). Installation is can be done with your favourite package manager. For example:

```bash
pip install ebike-connect
```

## Usage

Initialize a client with your username and password:
```python
from ebikeconnect.client import EBikeConnectClient


client = EBikeConnectClient.login("username", "password")
```

The eBike Connect api provides `rides` and `trips`, where a ride is a single uninterrupted ride, and a trip is a collection of rides (all rides on a single day?).

Rides and trips can be listed with the following methods:

```python
def find_rides(
    self, from_datetime: datetime | None = None, to_datetime: datetime | None = None
) -> Iterable[EBikeConnectRide]
```

This returns an iterable of `EBikeConnectRide` dataclasses, which have the following fields:
```python
    id: str
    start_time: datetime
    end_time: datetime
    driving_time: timedelta
    type: str
    status: int
    total_distance: float
    title: str
    calories: float
    avg_speed: float
    max_speed: float
```

```python
def find_trips(
    self, from_datetime: datetime | None = None, to_datetime: datetime | None = None
) -> Iterable[EBikeConnectTrip]:
```

This returns an iterable of `EBikeConnectTrip` dataclasses, which have the following fields:
```python
    id: str
    start_time: datetime
    end_time: datetime
    driving_time: timedelta
    type: str
    status: int
    total_distance: float
    ride_ids: list[str]
```


In addition, ride details (with many additional fields) can be obtained by calling:

```python
def get_ride(self, id: str) -> EBikeConnectRideDetails
```

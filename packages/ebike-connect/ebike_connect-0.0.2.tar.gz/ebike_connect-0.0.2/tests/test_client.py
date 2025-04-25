from itertools import islice

import pytest
from requests.exceptions import HTTPError

from ebikeconnect import EBikeConnectClient


class TestClient:
    def test_invalid_authentication(self):
        with pytest.raises(HTTPError) as exc:
            EBikeConnectClient.login("username", "password")
        assert exc.value.response.status_code == 403
        assert "403 Client Error" in str(exc.value)

    def test_user_agent(self):
        with pytest.raises(HTTPError) as exc:
            EBikeConnectClient.login("username", "password")
        assert exc.value.response.request.headers["User-Agent"].startswith("python-ebikeconnect/")

    def test_get_trip(self, client: EBikeConnectClient):
        with pytest.raises(NotImplementedError):
            client.get_trip("abcd")


class TestAuthenticatedClient:
    def test_cookie(self, authenticated_client: EBikeConnectClient):
        assert len(authenticated_client.cookie) > 30

    def test_find_rides(self, authenticated_client: EBikeConnectClient):
        rides = list(islice(authenticated_client.find_rides(), 6))
        assert len(rides) == 6, "Please ensure you have at least 6 rides."
        ride_ids = {ride.id for ride in rides}
        assert len(ride_ids) == 6  # Verify that paging does not result in duplicates.
        # Now create a new request, skipping the first two results.
        other_rides = list(islice(authenticated_client.find_rides(to_datetime=rides[2].end_time), 4))
        assert len(other_rides) == 4
        other_ride_ids = {ride.id for ride in other_rides}
        assert rides[0].id not in other_ride_ids
        assert rides[1].id not in other_ride_ids
        assert other_ride_ids.issubset(ride_ids)  # Verify paging did not skip a ride.

    def test_find_trips(self, authenticated_client: EBikeConnectClient):
        trips = list(islice(authenticated_client.find_trips(), 6))
        assert len(trips) == 6, "Please ensure you have at least 6 trips."
        trip_ids = {trip.id for trip in trips}
        assert len(trip_ids) == 6  # Verify that paging does not result in duplicates.
        # Now create a new request, skipping the first two results.
        other_trips = list(islice(authenticated_client.find_trips(to_datetime=trips[2].end_time), 4))
        assert len(other_trips) == 4
        other_trip_ids = {ride.id for ride in other_trips}
        assert trips[0].id not in other_trip_ids
        assert trips[1].id not in other_trip_ids
        assert other_trip_ids.issubset(trip_ids)  # Verify paging did not skip a trip.

    def test_get_ride(self, authenticated_client: EBikeConnectClient):
        rides = authenticated_client.find_rides()
        id = next(iter(rides)).id
        ride_details = authenticated_client.get_ride(id)
        assert ride_details.id == id

    def test_get_nonexistent_ride(self, authenticated_client: EBikeConnectClient):
        with pytest.raises(HTTPError) as exc:
            authenticated_client.get_ride("1234")
        assert exc.value.response.status_code == 400

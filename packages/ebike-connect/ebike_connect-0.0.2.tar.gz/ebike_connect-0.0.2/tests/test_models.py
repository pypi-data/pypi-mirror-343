from datetime import datetime

from ebikeconnect.models import EBikeConnectActivity


class TestActivity:
    def test_init(self):
        activity = EBikeConnectActivity(
            **{
                "id": "12345678",
                "start_time": "1723304159000",
                "end_time": "1723304416000",
                "driving_time": "254000",
                "type": "BIKE_RIDE",
                "status": 1,
                "total_distance": 1207.0,
            }
        )
        assert isinstance(activity.start_time, datetime)

import datetime
from json import JSONEncoder


class DatetimeEncoder(JSONEncoder):
    def default(self, o: datetime.datetime) -> str:
        return o.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

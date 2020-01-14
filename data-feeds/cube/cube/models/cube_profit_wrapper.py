# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = cube_profit_wrapper_from_dict(json.loads(json_string))

from datetime import datetime
from typing import Any, List, Optional
from cube.models.wrapper_util import *


class CubeProfitWrapperElement:
    time: Optional[int]
    date: Optional[datetime]
    value: Optional[float]
    percent: Optional[float]

    def __init__(self, time: Optional[int], date: Optional[datetime], value: Optional[float], percent: Optional[float]) -> None:
        self.time = time
        self.date = date
        self.value = value
        self.percent = percent

    @staticmethod
    def from_dict(obj: Any) -> 'CubeProfitWrapperElement':
        assert isinstance(obj, dict)
        time = from_union([from_int, from_none], obj.get("time"))
        date = from_union([from_datetime, from_none], obj.get("date"))
        value = from_union([from_float, from_none], obj.get("value"))
        percent = from_union([from_float, from_none], obj.get("percent"))
        return CubeProfitWrapperElement(time, date, value, percent)

    def to_dict(self) -> dict:
        result: dict = {}
        result["time"] = from_union([from_int, from_none], self.time)
        result["date"] = from_union([lambda x: x.isoformat(), from_none], self.date)
        result["value"] = from_union([to_float, from_none], self.value)
        result["percent"] = from_union([to_float, from_none], self.percent)
        return result


def cube_profit_wrapper_from_dict(s: Any) -> List[CubeProfitWrapperElement]:
    return from_list(CubeProfitWrapperElement.from_dict, s)


def cube_profit_wrapper_to_dict(x: List[CubeProfitWrapperElement]) -> Any:
    return from_list(lambda x: to_class(CubeProfitWrapperElement, x), x)

# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = cube_item_wrapper_from_dict(json.loads(json_string))

from typing import Optional, Any, List
from cube.models.wrapper_util import *


class CubeItemWrapper:
    symbol: Optional[str]
    market: Optional[str]
    name: Optional[str]
    net_value: Optional[float]
    closed_at: Optional[int]

    def __init__(self, symbol: Optional[str], market: Optional[str], name: Optional[str], net_value: Optional[float], closed_at: Optional[int]) -> None:
        self.symbol = symbol
        self.market = market
        self.name = name
        self.net_value = net_value
        self.closed_at = closed_at

    @staticmethod
    def from_dict(obj: Any) -> 'CubeItemWrapper':
        assert isinstance(obj, dict)
        symbol = from_union([from_str, from_none], obj.get("symbol"))
        market = from_union([from_str, from_none], obj.get("market"))
        name = from_union([from_str, from_none], obj.get("name"))
        net_value = from_union([from_float, from_none], obj.get("net_value"))
        closed_at = from_union([from_int, from_none], obj.get("closed_at"))
        return CubeItemWrapper(symbol, market, name, net_value, closed_at)

    def to_dict(self) -> dict:
        result: dict = {}
        result["symbol"] = from_union([from_str, from_none], self.symbol)
        result["market"] = from_union([from_str, from_none], self.market)
        result["name"] = from_union([from_str, from_none], self.name)
        result["net_value"] = from_union([to_float, from_none], self.net_value)
        result["closed_at"] = from_union([from_int, from_none], self.closed_at)
        return result


def cube_item_wrapper_from_dict(s: Any) -> List[CubeItemWrapper]:
    return from_list(CubeItemWrapper.from_dict, s)


def cube_item_wrapper_to_dict(x: List[CubeItemWrapper]) -> Any:
    return from_list(lambda x: to_class(CubeItemWrapper, x), x)

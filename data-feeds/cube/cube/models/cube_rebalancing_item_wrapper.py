# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = cube_rebalance_item_wrapper_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List
from cube.models.wrapper_util import *


@dataclass
class CubeRebalanceItemWrapper:
    holdings: None
    rebalance_id: Optional[int] = None
    status: Optional[str] = None
    cube_id: Optional[int] = None
    prev_bebalancing_id: Optional[int] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    cash_value: Optional[float] = None
    cash: Optional[float] = None
    comment: Optional[str] = None
    diff: Optional[float] = None
    new_buy_count: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'CubeRebalanceItemWrapper':
        assert isinstance(obj, dict)
        holdings = from_none(obj.get("holdings"))
        rebalance_id = from_union([from_int, from_none], obj.get("id"))
        status = from_union([from_str, from_none], obj.get("status"))
        cube_id = from_union([from_int, from_none], obj.get("cube_id"))
        prev_bebalancing_id = from_union([from_int, from_none_of_int], obj.get("prev_bebalancing_id"))
        created_at = from_union([from_int, from_none], obj.get("created_at"))
        updated_at = from_union([from_int, from_none], obj.get("updated_at"))
        cash_value = from_union([from_float, from_none_of_float], obj.get("cash_value"))
        cash = from_union([from_float, from_none_of_float], obj.get("cash"))
        comment = from_union([from_str, from_none], obj.get("comment"))
        diff = from_union([from_float, from_none_of_float], obj.get("diff"))
        new_buy_count = from_union([from_int, from_none_of_int], obj.get("new_buy_count"))
        return CubeRebalanceItemWrapper(holdings, rebalance_id, status, cube_id, prev_bebalancing_id, created_at,
                                        updated_at, cash_value, cash, comment, diff, new_buy_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["holdings"] = from_none(self.holdings)
        result["rebalance_id"] = from_union([from_int, from_none], self.rebalance_id)
        result["status"] = from_union([from_str, from_none], self.status)
        result["cube_id"] = from_union([from_int, from_none], self.cube_id)
        result["prev_bebalancing_id"] = from_union([from_int, from_none_of_int], self.prev_bebalancing_id)
        result["created_at"] = from_union([from_int, from_none], self.created_at)
        result["updated_at"] = from_union([from_int, from_none], self.updated_at)
        result["cash_value"] = from_union([to_float, from_none_of_float], self.cash_value)
        result["cash"] = from_union([to_float, from_none_of_float], self.cash)
        result["comment"] = from_union([from_str, from_none], self.comment)
        result["diff"] = from_union([to_float, from_none_of_float], self.diff)
        result["new_buy_count"] = from_union([from_int, from_none_of_int], self.new_buy_count)
        return result


def cube_rebalance_item_wrapper_from_dict(s: Any) -> List[CubeRebalanceItemWrapper]:
    return from_list(CubeRebalanceItemWrapper.from_dict, s)


def cube_rebalance_item_wrapper_to_dict(x: List[CubeRebalanceItemWrapper]) -> Any:
    return from_list(lambda x: to_class(CubeRebalanceItemWrapper, x), x)

# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = cube_rebalance_history_item_wrapper_from_dict(json.loads(json_string))

from dataclasses import dataclass
from typing import Optional, Any, List
from cube.models.wrapper_util import *


@dataclass
class CubeRebalanceHistoryItemWrapper:
    id: Optional[int] = None
    rebalancing_id: Optional[int] = None
    stock_id: Optional[int] = None
    stock_name: Optional[str] = None
    stock_symbol: Optional[str] = None
    volume: Optional[float] = None
    price: Optional[float] = None
    net_value: Optional[float] = None
    weight: Optional[float] = None
    target_weight: Optional[float] = None
    prev_weight: Optional[float] = None
    prev_target_weight: Optional[float] = None
    prev_weight_adjusted: Optional[float] = None
    prev_volume: Optional[float] = None
    prev_price: Optional[float] = None
    prev_net_value: Optional[float] = None
    proactive: Optional[bool] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    target_volume: Optional[float] = None
    prev_target_volume: Optional[float] = None

    @staticmethod
    def from_dict(obj: Any) -> 'CubeRebalanceHistoryItemWrapper':
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        rebalancing_id = from_union([from_int, from_none], obj.get("rebalancing_id"))
        stock_id = from_union([from_int, from_none], obj.get("stock_id"))
        stock_name = from_union([from_str, from_none], obj.get("stock_name"))
        stock_symbol = from_union([from_str, from_none], obj.get("stock_symbol"))
        volume = from_union([from_float, from_none_of_float], obj.get("volume"))
        price = from_union([from_float, from_none_of_float], obj.get("price"))
        net_value = from_union([from_float, from_none_of_float], obj.get("net_value"))
        weight = from_union([from_float, from_none_of_float], obj.get("weight"))
        target_weight = from_union([from_float, from_none_of_float], obj.get("target_weight"))
        prev_weight = from_union([from_float, from_none_of_float], obj.get("prev_weight"))
        prev_target_weight = from_union([from_float, from_none_of_float], obj.get("prev_target_weight"))
        prev_weight_adjusted = from_union([from_float, from_none_of_float], obj.get("prev_weight_adjusted"))
        prev_volume = from_union([from_float, from_none_of_float], obj.get("prev_volume"))
        prev_price = from_union([from_float, from_none_of_float], obj.get("prev_price"))
        prev_net_value = from_union([from_float, from_none_of_float], obj.get("prev_net_value"))
        proactive = from_union([from_bool, from_none], obj.get("proactive"))
        created_at = from_union([from_int, from_none], obj.get("created_at"))
        updated_at = from_union([from_int, from_none], obj.get("updated_at"))
        target_volume = from_union([from_float, from_none_of_float], obj.get("target_volume"))
        prev_target_volume = from_union([from_float, from_none_of_float], obj.get("prev_target_volume"))
        return CubeRebalanceHistoryItemWrapper(id, rebalancing_id, stock_id, stock_name, stock_symbol, volume, price,
                                               net_value, weight, target_weight, prev_weight, prev_target_weight,
                                               prev_weight_adjusted, prev_volume, prev_price, prev_net_value, proactive,
                                               created_at, updated_at, target_volume, prev_target_volume)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_int, from_none], self.id)
        result["rebalancing_id"] = from_union([from_int, from_none], self.rebalancing_id)
        result["stock_id"] = from_union([from_int, from_none], self.stock_id)
        result["stock_name"] = from_union([from_str, from_none], self.stock_name)
        result["stock_symbol"] = from_union([from_str, from_none], self.stock_symbol)
        result["volume"] = from_union([to_float, from_none_of_float], self.volume)
        result["price"] = from_union([to_float, from_none_of_float], self.price)
        result["net_value"] = from_union([to_float, from_none_of_float], self.net_value)
        result["weight"] = from_union([to_float, from_none_of_float], self.weight)
        result["target_weight"] = from_union([to_float, from_none_of_float], self.target_weight)
        result["prev_weight"] = from_union([to_float, from_none_of_float], self.prev_weight)
        result["prev_target_weight"] = from_union([to_float, from_none_of_float], self.prev_target_weight)
        result["prev_weight_adjusted"] = from_union([to_float, from_none_of_float], self.prev_weight_adjusted)
        result["prev_volume"] = from_union([to_float, from_none_of_float], self.prev_volume)
        result["prev_price"] = from_union([to_float, from_none_of_float], self.prev_price)
        result["prev_net_value"] = from_union([to_float, from_none_of_float], self.prev_net_value)
        result["proactive"] = from_union([from_bool, from_none], self.proactive)
        result["created_at"] = from_union([from_int, from_none], self.created_at)
        result["updated_at"] = from_union([from_int, from_none], self.updated_at)
        result["target_volume"] = from_union([to_float, from_none_of_float], self.target_volume)
        result["prev_target_volume"] = from_union([to_float, from_none_of_float], self.prev_target_volume)
        return result


def cube_rebalance_history_item_wrapper_from_dict(s: Any) -> List[CubeRebalanceHistoryItemWrapper]:
    return from_list(CubeRebalanceHistoryItemWrapper.from_dict, s)


def cube_rebalance_history_item_wrapper_to_dict(x: List[CubeRebalanceHistoryItemWrapper]) -> Any:
    return from_list(lambda x: to_class(CubeRebalanceHistoryItemWrapper, x), x)

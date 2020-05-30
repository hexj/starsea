# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = page_from_dict(json.loads(json_string))

from enum import Enum
from dataclasses import dataclass
from typing import Optional, Any, List, TypeVar, Callable, Type, cast


T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Category(Enum):
    USER_REBALANCING = "user_rebalancing"


class ExeStrategy(Enum):
    INTRADAY_ALL = "intraday_all"


@dataclass
class RebalancingHistory:
    id: Optional[int] = None
    rebalancing_id: Optional[int] = None
    stock_id: Optional[int] = None
    stock_name: Optional[str] = None
    stock_symbol: Optional[str] = None
    volume: Optional[float] = None
    price: Optional[float] = None
    net_value: Optional[float] = None
    weight: Optional[int] = None
    target_weight: Optional[int] = None
    prev_weight: Optional[int] = None
    prev_target_weight: Optional[int] = None
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
    def from_dict(obj: Any) -> 'RebalancingHistory':
        assert isinstance(obj, dict)
        id = from_union([from_int, from_none], obj.get("id"))
        rebalancing_id = from_union([from_int, from_none], obj.get("rebalancing_id"))
        stock_id = from_union([from_int, from_none], obj.get("stock_id"))
        stock_name = from_union([from_str, from_none], obj.get("stock_name"))
        stock_symbol = from_union([from_str, from_none], obj.get("stock_symbol"))
        volume = from_union([from_float, from_none], obj.get("volume"))
        price = from_union([from_float, from_none], obj.get("price"))
        net_value = from_union([from_float, from_none], obj.get("net_value"))
        weight = from_union([from_int, from_none], obj.get("weight"))
        target_weight = from_union([from_int, from_none], obj.get("target_weight"))
        prev_weight = from_union([from_int, from_none], obj.get("prev_weight"))
        prev_target_weight = from_union([from_int, from_none], obj.get("prev_target_weight"))
        prev_weight_adjusted = from_union([from_float, from_none], obj.get("prev_weight_adjusted"))
        prev_volume = from_union([from_float, from_none], obj.get("prev_volume"))
        prev_price = from_union([from_float, from_none], obj.get("prev_price"))
        prev_net_value = from_union([from_float, from_none], obj.get("prev_net_value"))
        proactive = from_union([from_bool, from_none], obj.get("proactive"))
        created_at = from_union([from_int, from_none], obj.get("created_at"))
        updated_at = from_union([from_int, from_none], obj.get("updated_at"))
        target_volume = from_union([from_float, from_none], obj.get("target_volume"))
        prev_target_volume = from_union([from_float, from_none], obj.get("prev_target_volume"))
        return RebalancingHistory(id, rebalancing_id, stock_id, stock_name, stock_symbol, volume, price, net_value, weight, target_weight, prev_weight, prev_target_weight, prev_weight_adjusted, prev_volume, prev_price, prev_net_value, proactive, created_at, updated_at, target_volume, prev_target_volume)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_union([from_int, from_none], self.id)
        result["rebalancing_id"] = from_union([from_int, from_none], self.rebalancing_id)
        result["stock_id"] = from_union([from_int, from_none], self.stock_id)
        result["stock_name"] = from_union([from_str, from_none], self.stock_name)
        result["stock_symbol"] = from_union([from_str, from_none], self.stock_symbol)
        result["volume"] = from_union([to_float, from_none], self.volume)
        result["price"] = from_union([to_float, from_none], self.price)
        result["net_value"] = from_union([to_float, from_none], self.net_value)
        result["weight"] = from_union([from_int, from_none], self.weight)
        result["target_weight"] = from_union([from_int, from_none], self.target_weight)
        result["prev_weight"] = from_union([from_int, from_none], self.prev_weight)
        result["prev_target_weight"] = from_union([from_int, from_none], self.prev_target_weight)
        result["prev_weight_adjusted"] = from_union([to_float, from_none], self.prev_weight_adjusted)
        result["prev_volume"] = from_union([to_float, from_none], self.prev_volume)
        result["prev_price"] = from_union([to_float, from_none], self.prev_price)
        result["prev_net_value"] = from_union([to_float, from_none], self.prev_net_value)
        result["proactive"] = from_union([from_bool, from_none], self.proactive)
        result["created_at"] = from_union([from_int, from_none], self.created_at)
        result["updated_at"] = from_union([from_int, from_none], self.updated_at)
        result["target_volume"] = from_union([to_float, from_none], self.target_volume)
        result["prev_target_volume"] = from_union([to_float, from_none], self.prev_target_volume)
        return result


class Status(Enum):
    SUCCESS = "success"


@dataclass
class ListElement:
    error_code: None
    error_message: None
    error_status: None
    holdings: None
    id: Optional[int] = None
    status: Optional[Status] = None
    cube_id: Optional[int] = None
    prev_bebalancing_id: Optional[int] = None
    category: Optional[Category] = None
    exe_strategy: Optional[ExeStrategy] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    cash_value: Optional[float] = None
    cash: Optional[int] = None
    rebalancing_histories: Optional[List[RebalancingHistory]] = None
    comment: Optional[str] = None
    diff: Optional[int] = None
    new_buy_count: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'ListElement':
        assert isinstance(obj, dict)
        error_code = from_none(obj.get("error_code"))
        error_message = from_none(obj.get("error_message"))
        error_status = from_none(obj.get("error_status"))
        holdings = from_none(obj.get("holdings"))
        id = from_union([from_int, from_none], obj.get("id"))
        status = from_union([Status, from_none], obj.get("status"))
        cube_id = from_union([from_int, from_none], obj.get("cube_id"))
        prev_bebalancing_id = from_union([from_int, from_none], obj.get("prev_bebalancing_id"))
        category = from_union([Category, from_none], obj.get("category"))
        exe_strategy = from_union([ExeStrategy, from_none], obj.get("exe_strategy"))
        created_at = from_union([from_int, from_none], obj.get("created_at"))
        updated_at = from_union([from_int, from_none], obj.get("updated_at"))
        cash_value = from_union([from_float, from_none], obj.get("cash_value"))
        cash = from_union([from_int, from_none], obj.get("cash"))
        rebalancing_histories = from_union([lambda x: from_list(RebalancingHistory.from_dict, x), from_none], obj.get("rebalancing_histories"))
        comment = from_union([from_str, from_none], obj.get("comment"))
        diff = from_union([from_int, from_none], obj.get("diff"))
        new_buy_count = from_union([from_int, from_none], obj.get("new_buy_count"))
        return ListElement(error_code, error_message, error_status, holdings, id, status, cube_id, prev_bebalancing_id, category, exe_strategy, created_at, updated_at, cash_value, cash, rebalancing_histories, comment, diff, new_buy_count)

    def to_dict(self) -> dict:
        result: dict = {}
        result["error_code"] = from_none(self.error_code)
        result["error_message"] = from_none(self.error_message)
        result["error_status"] = from_none(self.error_status)
        result["holdings"] = from_none(self.holdings)
        result["id"] = from_union([from_int, from_none], self.id)
        result["status"] = from_union([lambda x: to_enum(Status, x), from_none], self.status)
        result["cube_id"] = from_union([from_int, from_none], self.cube_id)
        result["prev_bebalancing_id"] = from_union([from_int, from_none], self.prev_bebalancing_id)
        result["category"] = from_union([lambda x: to_enum(Category, x), from_none], self.category)
        result["exe_strategy"] = from_union([lambda x: to_enum(ExeStrategy, x), from_none], self.exe_strategy)
        result["created_at"] = from_union([from_int, from_none], self.created_at)
        result["updated_at"] = from_union([from_int, from_none], self.updated_at)
        result["cash_value"] = from_union([to_float, from_none], self.cash_value)
        result["cash"] = from_union([from_int, from_none], self.cash)
        result["rebalancing_histories"] = from_union([lambda x: from_list(lambda x: to_class(RebalancingHistory, x), x), from_none], self.rebalancing_histories)
        result["comment"] = from_union([from_str, from_none], self.comment)
        result["diff"] = from_union([from_int, from_none], self.diff)
        result["new_buy_count"] = from_union([from_int, from_none], self.new_buy_count)
        return result


@dataclass
class Page:
    count: Optional[int] = None
    page: Optional[int] = None
    total_count: Optional[int] = None
    list: Optional[List[ListElement]] = None
    max_page: Optional[int] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Page':
        assert isinstance(obj, dict)
        count = from_union([from_int, from_none], obj.get("count"))
        page = from_union([from_int, from_none], obj.get("page"))
        total_count = from_union([from_int, from_none], obj.get("totalCount"))
        list = from_union([lambda x: from_list(ListElement.from_dict, x), from_none], obj.get("list"))
        max_page = from_union([from_int, from_none], obj.get("maxPage"))
        return Page(count, page, total_count, list, max_page)

    def to_dict(self) -> dict:
        result: dict = {}
        result["count"] = from_union([from_int, from_none], self.count)
        result["page"] = from_union([from_int, from_none], self.page)
        result["totalCount"] = from_union([from_int, from_none], self.total_count)
        result["list"] = from_union([lambda x: from_list(lambda x: to_class(ListElement, x), x), from_none], self.list)
        result["maxPage"] = from_union([from_int, from_none], self.max_page)
        return result


def page_from_dict(s: Any) -> Page:
    return Page.from_dict(s)


def page_to_dict(x: Page) -> Any:
    return to_class(Page, x)

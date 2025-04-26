from dataclasses import dataclass, field
from enum import Enum, StrEnum
from typing import Any, Callable, Dict, List, Type, TypeVar, cast

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_float(x: Any) -> float:
    assert isinstance(x, (int, float))
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Data:
    data: float
    dotcount: int
    hasdata: bool
    strdata: str

    @staticmethod
    def from_dict(obj: Any) -> "Data":
        assert isinstance(obj, dict)
        data = from_float(obj.get("data"))
        dotcount = from_int(obj.get("dotcount"))
        hasdata = from_bool(obj.get("hasdata"))
        strdata = from_str(obj.get("strdata"))
        return Data(data, dotcount, hasdata, strdata)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data"] = to_float(self.data)
        result["dotcount"] = from_int(self.dotcount)
        result["hasdata"] = from_bool(self.hasdata)
        result["strdata"] = from_str(self.strdata)
        return result


class DimensionCode(StrEnum):
    SJ = "sj"
    ZB = "zb"


@dataclass
class DimensionRef:
    valuecode: str
    wdcode: DimensionCode

    @staticmethod
    def from_dict(obj: Any) -> "DimensionRef":
        assert isinstance(obj, dict)
        valuecode = from_str(obj.get("valuecode"))
        wdcode = DimensionCode(obj.get("wdcode"))
        return DimensionRef(valuecode, wdcode)

    def to_dict(self) -> dict:
        result: dict = {}
        result["valuecode"] = from_str(self.valuecode)
        result["wdcode"] = to_enum(DimensionCode, self.wdcode)
        return result


@dataclass
class DataNode:
    code: str
    data: Data
    wds: List[DimensionRef]

    def sj_code(self) -> str:
        return next(wd.valuecode for wd in self.wds if wd.wdcode == DimensionCode.SJ)

    def zb_code(self) -> str:
        return next(wd.valuecode for wd in self.wds if wd.wdcode == DimensionCode.ZB)

    @staticmethod
    def from_dict(obj: Any) -> "DataNode":
        assert isinstance(obj, dict)
        code = from_str(obj.get("code"))
        data = Data.from_dict(obj.get("data"))
        wds = from_list(DimensionRef.from_dict, obj.get("wds"))
        return DataNode(code, data, wds)

    def to_dict(self) -> dict:
        result: dict = {}
        result["code"] = from_str(self.code)
        result["data"] = to_class(Data, self.data)
        result["wds"] = from_list(lambda x: to_class(DimensionRef, x), self.wds)
        return result


@dataclass
class Node:
    cname: str
    code: str
    dotcount: int
    exp: str
    ifshowcode: bool
    memo: str
    name: str
    nodesort: int
    sortcode: int
    tag: str
    unit: str

    @staticmethod
    def from_dict(obj: Any) -> "Node":
        assert isinstance(obj, dict)
        cname = from_str(obj.get("cname"))
        code = from_str(obj.get("code"))
        dotcount = from_int(obj.get("dotcount"))
        exp = from_str(obj.get("exp"))
        ifshowcode = from_bool(obj.get("ifshowcode"))
        memo = from_str(obj.get("memo"))
        name = from_str(obj.get("name"))
        nodesort = int(from_str(obj.get("nodesort")))
        sortcode = from_int(obj.get("sortcode"))
        tag = from_str(obj.get("tag"))
        unit = from_str(obj.get("unit"))
        return Node(
            cname,
            code,
            dotcount,
            exp,
            ifshowcode,
            memo,
            name,
            nodesort,
            sortcode,
            tag,
            unit,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["cname"] = from_str(self.cname)
        result["code"] = from_str(self.code)
        result["dotcount"] = from_int(self.dotcount)
        result["exp"] = from_str(self.exp)
        result["ifshowcode"] = from_bool(self.ifshowcode)
        result["memo"] = from_str(self.memo)
        result["name"] = from_str(self.name)
        result["nodesort"] = from_str(str(self.nodesort))
        result["sortcode"] = from_int(self.sortcode)
        result["tag"] = from_str(self.tag)
        result["unit"] = from_str(self.unit)
        return result


@dataclass
class DimensionNodes:
    nodes: List[Node]
    wdcode: DimensionCode
    wdname: str

    @staticmethod
    def from_dict(obj: Any) -> "DimensionNodes":
        assert isinstance(obj, dict)
        nodes = from_list(Node.from_dict, obj.get("nodes"))
        wdcode = DimensionCode(obj.get("wdcode"))
        wdname = from_str(obj.get("wdname"))
        return DimensionNodes(nodes, wdcode, wdname)

    def to_dict(self) -> dict:
        result: dict = {}
        result["nodes"] = from_list(lambda x: to_class(Node, x), self.nodes)
        result["wdcode"] = to_enum(DimensionCode, self.wdcode)
        result["wdname"] = from_str(self.wdname)
        return result


@dataclass
class ReturnData:
    datanodes: List[DataNode]
    freshsort: int
    hasdatacount: int
    wdnodes: List[DimensionNodes]

    def zb_dimension(self) -> DimensionNodes:
        return next(wd for wd in self.wdnodes if wd.wdcode == DimensionCode.ZB)

    def sj_dimension(self) -> DimensionNodes:
        return next(wd for wd in self.wdnodes if wd.wdcode == DimensionCode.SJ)

    @staticmethod
    def from_dict(obj: Any) -> "ReturnData":
        assert isinstance(obj, dict)
        datanodes = from_list(DataNode.from_dict, obj.get("datanodes"))
        freshsort = from_int(obj.get("freshsort"))
        hasdatacount = from_int(obj.get("hasdatacount"))
        wdnodes = from_list(DimensionNodes.from_dict, obj.get("wdnodes"))
        return ReturnData(datanodes, freshsort, hasdatacount, wdnodes)

    def to_dict(self) -> dict:
        result: dict = {}
        result["datanodes"] = from_list(lambda x: to_class(DataNode, x), self.datanodes)
        result["freshsort"] = from_int(self.freshsort)
        result["hasdatacount"] = from_int(self.hasdatacount)
        result["wdnodes"] = from_list(
            lambda x: to_class(DimensionNodes, x), self.wdnodes
        )
        return result


@dataclass
class IndicatorNode:
    id: str
    name: str
    pid: str
    isParent: bool
    dbcode: str
    wdcode: str
    children: List["IndicatorNode"] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IndicatorNode":
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            pid=data.get("pid", ""),
            isParent=data.get("isParent", False),
            dbcode=data.get("dbcode", ""),
            wdcode=data.get("wdcode", ""),
        )

    # from the response of get_tree, which is list[dict]
    @classmethod
    def from_list(cls, data: List[Dict[str, Any]]) -> List["IndicatorNode"]:
        return [cls.from_dict(item) for item in data]

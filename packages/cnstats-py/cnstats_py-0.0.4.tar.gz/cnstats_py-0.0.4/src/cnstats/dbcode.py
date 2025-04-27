from enum import StrEnum


class DBCode(StrEnum):
    hgyd = "月度数据"
    hgjd = "季度数据"
    hgnd = "年度数据"

    def __str__(self) -> str:
        return f"{self.name}({self.value})"

    def __repr__(self) -> str:
        return f"DBCode.{self.name}('{self.value}')"

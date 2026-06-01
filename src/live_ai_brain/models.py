from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class TaskStatus(StrEnum):
    PENDING = "待确认"
    ADOPTED = "已采纳"
    EXECUTED = "已执行"
    VERIFIED = "已验证"
    INVALID = "无效"


@dataclass(frozen=True)
class LiveMetrics:
    product_name: str
    live_date: str
    time_slot: str
    host: str
    controller: str
    activity_price: str
    benefits: str
    viewers: int
    avg_stay_seconds: float
    interactions: int
    product_clicks: int
    orders: int
    revenue: float


@dataclass(frozen=True)
class QianchuanMetrics:
    spend: float
    click_rate: float
    conversion_rate: float
    roi: float
    cost_per_order: float
    main_material: str


@dataclass(frozen=True)
class AssetRecord:
    session_id: str
    asset_type: str
    source: str
    url_or_path: str
    note: str


@dataclass(frozen=True)
class ExecutionTask:
    id: str
    session_id: str
    owner_role: str
    title: str
    detail: str
    status: TaskStatus = TaskStatus.PENDING

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["status"] = str(self.status)
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExecutionTask":
        return cls(
            id=str(data["id"]),
            session_id=str(data["session_id"]),
            owner_role=str(data["owner_role"]),
            title=str(data["title"]),
            detail=str(data["detail"]),
            status=TaskStatus(str(data.get("status", TaskStatus.PENDING))),
        )

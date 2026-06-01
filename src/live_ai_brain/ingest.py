from __future__ import annotations

from pathlib import Path

import pandas as pd

from live_ai_brain.models import LiveMetrics, QianchuanMetrics


def _first_row(path: Path | str) -> dict[str, object]:
    file_path = Path(path)
    if file_path.suffix.lower() in {".xlsx", ".xls"}:
        frame = pd.read_excel(file_path)
    else:
        frame = pd.read_csv(file_path)
    if frame.empty:
        raise ValueError(f"{file_path} 没有数据行")
    return frame.iloc[0].to_dict()


def _text(row: dict[str, object], key: str) -> str:
    value = row.get(key, "")
    return "" if pd.isna(value) else str(value)


def _int(row: dict[str, object], key: str) -> int:
    value = row.get(key, 0)
    return 0 if pd.isna(value) else int(float(value))


def _float(row: dict[str, object], key: str) -> float:
    value = row.get(key, 0)
    return 0.0 if pd.isna(value) else float(value)


def parse_live_metrics_csv(path: Path | str) -> LiveMetrics:
    row = _first_row(path)
    return LiveMetrics(
        product_name=_text(row, "产品名称"),
        live_date=_text(row, "直播日期"),
        time_slot=_text(row, "直播时段"),
        host=_text(row, "主播"),
        controller=_text(row, "场控"),
        activity_price=_text(row, "活动价格"),
        benefits=_text(row, "权益"),
        viewers=_int(row, "进入人数"),
        avg_stay_seconds=_float(row, "平均停留秒"),
        interactions=_int(row, "互动数"),
        product_clicks=_int(row, "商品点击"),
        orders=_int(row, "成交数"),
        revenue=_float(row, "成交额"),
    )


def parse_qianchuan_metrics_csv(path: Path | str) -> QianchuanMetrics:
    row = _first_row(path)
    return QianchuanMetrics(
        spend=_float(row, "消耗"),
        click_rate=_float(row, "点击率"),
        conversion_rate=_float(row, "转化率"),
        roi=_float(row, "ROI"),
        cost_per_order=_float(row, "成交成本"),
        main_material=_text(row, "主投素材"),
    )

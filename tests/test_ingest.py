from pathlib import Path

import pandas as pd
import pytest

from live_ai_brain.ingest import parse_live_metrics_csv, parse_qianchuan_metrics_csv


def test_parse_live_metrics_csv_maps_required_fields(tmp_path: Path):
    path = tmp_path / "live.csv"
    pd.DataFrame(
        [
            {
                "产品名称": "窦神文言文速通",
                "直播日期": "2026-06-01",
                "直播时段": "19:00-21:00",
                "主播": "主播A",
                "场控": "场控B",
                "活动价格": "199",
                "权益": "直播课+纸质资料",
                "进入人数": 1000,
                "平均停留秒": 38.5,
                "互动数": 120,
                "商品点击": 80,
                "成交数": 12,
                "成交额": 2388,
            }
        ]
    ).to_csv(path, index=False, encoding="utf-8-sig")

    metrics = parse_live_metrics_csv(path)

    assert metrics.product_name == "窦神文言文速通"
    assert metrics.product_clicks == 80
    assert metrics.revenue == 2388


def test_parse_qianchuan_metrics_csv_maps_required_fields_and_defaults_na(tmp_path: Path):
    path = tmp_path / "qianchuan.csv"
    pd.DataFrame(
        [
            {
                "消耗": "",
                "点击率": "0.125",
                "转化率": 0.032,
                "ROI": "2.8",
                "成交成本": 43,
                "主投素材": "material-a.mp4",
            }
        ]
    ).to_csv(path, index=False, encoding="utf-8-sig")

    metrics = parse_qianchuan_metrics_csv(path)

    assert metrics.spend == 0.0
    assert metrics.click_rate == 0.125
    assert metrics.conversion_rate == 0.032
    assert metrics.roi == 2.8
    assert metrics.cost_per_order == 43.0
    assert metrics.main_material == "material-a.mp4"


def test_parse_qianchuan_metrics_csv_rejects_truly_empty_csv(tmp_path: Path):
    path = tmp_path / "empty.csv"
    path.write_text("", encoding="utf-8")

    with pytest.raises(ValueError) as exc_info:
        parse_qianchuan_metrics_csv(path)

    assert str(exc_info.value) == f"{path} 没有数据行"

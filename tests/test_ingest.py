from pathlib import Path

import pandas as pd

from live_ai_brain.ingest import parse_live_metrics_csv


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

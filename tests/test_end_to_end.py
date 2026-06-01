from pathlib import Path

from live_ai_brain.content import generate_live_script_pack
from live_ai_brain.ingest import parse_live_metrics_csv, parse_qianchuan_metrics_csv
from live_ai_brain.replay import build_replay_report


def test_end_to_end_replay_to_content_generation():
    fixture_dir = Path("tests") / "fixtures"
    live = parse_live_metrics_csv(fixture_dir / "live_metrics.csv")
    qianchuan = parse_qianchuan_metrics_csv(fixture_dir / "qianchuan_metrics.csv")
    report = build_replay_report(live, qianchuan)
    script = generate_live_script_pack(
        product_name=live.product_name,
        pain_point="孩子文言文翻译靠猜",
        benefit=live.benefits,
    )

    assert "商品点击偏弱" in report.summary
    assert "开场留人" in script
    assert live.product_name in script

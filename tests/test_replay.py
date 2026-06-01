from live_ai_brain.models import LiveMetrics, QianchuanMetrics
from live_ai_brain.replay import build_replay_report


def test_build_replay_report_prioritizes_low_click_rate():
    live = LiveMetrics(
        product_name="窦神文言文速通",
        live_date="2026-06-01",
        time_slot="19:00-21:00",
        host="主播A",
        controller="场控B",
        activity_price="199",
        benefits="直播课+纸质资料",
        viewers=1000,
        avg_stay_seconds=45,
        interactions=200,
        product_clicks=20,
        orders=2,
        revenue=398,
    )
    qianchuan = QianchuanMetrics(
        spend=800,
        click_rate=0.8,
        conversion_rate=0.1,
        roi=0.5,
        cost_per_order=400,
        main_material="文言文痛点口播",
    )

    report = build_replay_report(live, qianchuan)

    assert "商品点击偏弱" in report.summary
    assert any("贴片" in action for action in report.next_actions)

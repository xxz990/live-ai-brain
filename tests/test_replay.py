from live_ai_brain.models import LiveMetrics, QianchuanMetrics
from live_ai_brain.replay import build_replay_report


def _live_metrics(
    *,
    viewers: int = 1000,
    product_clicks: int = 200,
    orders: int = 40,
) -> LiveMetrics:
    return LiveMetrics(
        product_name="窦神文言文速通",
        live_date="2026-06-01",
        time_slot="19:00-21:00",
        host="主播A",
        controller="场控B",
        activity_price="199",
        benefits="直播课+纸质资料",
        viewers=viewers,
        avg_stay_seconds=45,
        interactions=200,
        product_clicks=product_clicks,
        orders=orders,
        revenue=398,
    )


def _qianchuan_metrics(*, roi: float = 1.5) -> QianchuanMetrics:
    return QianchuanMetrics(
        spend=800,
        click_rate=0.8,
        conversion_rate=0.1,
        roi=roi,
        cost_per_order=400,
        main_material="文言文痛点口播",
    )


def test_build_replay_report_prioritizes_low_click_rate():
    report = build_replay_report(
        _live_metrics(product_clicks=20, orders=2),
        _qianchuan_metrics(roi=0.5),
    )

    assert "商品点击偏弱" in report.summary
    assert any("贴片" in action for action in report.next_actions)


def test_build_replay_report_uses_zero_click_diagnosis_without_conversion_claim():
    report = build_replay_report(
        _live_metrics(product_clicks=0, orders=0),
        _qianchuan_metrics(),
    )

    assert any("商品点击为零" in diagnosis for diagnosis in report.diagnoses)
    assert any("先恢复商品点击" in action for action in report.next_actions)
    assert "点击后成交偏弱" not in report.summary
    assert not any("点击后成交偏弱" in diagnosis for diagnosis in report.diagnoses)


def test_build_replay_report_does_not_flag_threshold_boundaries():
    report = build_replay_report(
        _live_metrics(viewers=1000, product_clicks=50, orders=8),
        _qianchuan_metrics(roi=1),
    )

    assert "商品点击偏弱" not in report.summary
    assert "点击后成交偏弱" not in report.summary
    assert "千川 ROI 偏低" not in report.summary
    assert "核心指标未触发明显风险" in report.summary


def test_build_replay_report_handles_zero_viewers_without_low_conversion():
    report = build_replay_report(
        _live_metrics(viewers=0, product_clicks=0, orders=0),
        _qianchuan_metrics(),
    )

    assert any("商品点击为零" in diagnosis for diagnosis in report.diagnoses)
    assert "点击后成交偏弱" not in report.summary

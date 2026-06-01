from __future__ import annotations

from dataclasses import dataclass

from live_ai_brain.models import LiveMetrics, QianchuanMetrics


@dataclass(frozen=True)
class ReplayReport:
    summary: str
    diagnoses: list[str]
    next_actions: list[str]


def build_replay_report(live: LiveMetrics, qianchuan: QianchuanMetrics) -> ReplayReport:
    diagnoses: list[str] = []
    actions: list[str] = []
    click_rate = live.product_clicks / live.viewers if live.viewers else 0
    order_rate = live.orders / live.product_clicks if live.product_clicks else 0

    if live.product_clicks == 0:
        diagnoses.append("商品点击为零：用户没有进入商品承接链路，暂不能判断点击后成交能力。")
        actions.append("先恢复商品点击，强化贴片、场控提醒和下单路径口播。")
    elif click_rate < 0.05:
        diagnoses.append("商品点击偏弱：用户进入后没有被充分引导点击商品。")
        actions.append("强化贴片和场控提醒，在讲到权益和下单流程时明确引导点击商品。")
    if live.product_clicks > 0 and order_rate < 0.15:
        diagnoses.append("点击后成交偏弱：用户可能仍有价格、权益或效果疑虑。")
        actions.append("补充异议处理话术，重点回答适合年级、课程权益和激活流程。")
    if qianchuan.roi < 1:
        diagnoses.append("千川 ROI 偏低：投放素材或直播承接需要调整。")
        actions.append("产出痛点版和方法版短视频脚本，分别测试点击率和转化率。")

    if not diagnoses:
        diagnoses.append("核心指标未触发明显风险，建议保留本场有效动作。")
        actions.append("沉淀本场话术和素材版本，下一场继续验证。")

    return ReplayReport(
        summary="；".join(item.split("：")[0] for item in diagnoses),
        diagnoses=diagnoses,
        next_actions=actions,
    )

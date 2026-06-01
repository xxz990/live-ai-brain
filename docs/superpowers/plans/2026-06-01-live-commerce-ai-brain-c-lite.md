# Live Commerce AI Brain C-lite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local single-user MVP for the C-lite live commerce AI brain: upload data, parse product knowledge, generate replay reports/content drafts, track execution tasks, and run basic compliance checks.

**Architecture:** Use a Streamlit app as the first working interface, backed by small Python modules with clear boundaries. Keep AI calls behind a provider interface so the app works in mock mode without credentials and can later use the OpenAI Responses API or another provider.

**Tech Stack:** Python 3.11+, Streamlit, pandas, openpyxl, python-docx, pypdf, pytest, dataclasses, JSON file storage.

---

## Scope Check

The approved spec covers several future subsystems. This implementation plan intentionally builds only the first local MVP:

- In scope: local uploads, Feishu/Baidu link registration, product knowledge loading from repository files, replay report generation, content draft generation, compliance checking, execution task tracking, JSON persistence.
- Out of scope for this plan: Feishu API sync, Baidu Netdisk automatic download, automatic video transcription, automatic Qianchuan account changes, multi-user auth, real-time livestream control.

## File Structure

- Create `pyproject.toml`: project metadata and dependencies.
- Create `src/live_ai_brain/__init__.py`: package marker.
- Create `src/live_ai_brain/models.py`: dataclasses for products, sessions, metrics, assets, generated outputs, tasks.
- Create `src/live_ai_brain/storage.py`: JSON persistence under `data/`.
- Create `src/live_ai_brain/knowledge.py`: load markdown/txt product knowledge and provide simple keyword retrieval.
- Create `src/live_ai_brain/ingest.py`: parse CSV/XLSX files and register links/assets.
- Create `src/live_ai_brain/compliance.py`: detect risky claims and suggest safer wording.
- Create `src/live_ai_brain/replay.py`: deterministic replay diagnosis from metrics.
- Create `src/live_ai_brain/content.py`: generate structured prompts and mock drafts for live scripts, short videos, and KT/overlay copy.
- Create `src/live_ai_brain/app.py`: Streamlit UI.
- Create `tests/`: focused unit tests for parsing, knowledge retrieval, compliance, replay, and content output.
- Create `data/.gitkeep`: local persistence directory marker.

## Task 1: Project Scaffold

**Files:**
- Create: `pyproject.toml`
- Create: `src/live_ai_brain/__init__.py`
- Create: `data/.gitkeep`
- Create: `tests/test_scaffold.py`

- [ ] **Step 1: Create package scaffold and dependency metadata**

Add this `pyproject.toml`:

```toml
[project]
name = "live-commerce-ai-brain"
version = "0.1.0"
description = "C-lite MVP for live commerce AI operations"
requires-python = ">=3.11"
dependencies = [
  "streamlit>=1.35",
  "pandas>=2.2",
  "openpyxl>=3.1",
  "python-docx>=1.1",
  "pypdf>=4.2",
]

[project.optional-dependencies]
dev = ["pytest>=8.2"]

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

Create `src/live_ai_brain/__init__.py`:

```python
"""Live commerce AI brain MVP package."""
```

Create `data/.gitkeep` as an empty file.

- [ ] **Step 2: Add scaffold test**

Create `tests/test_scaffold.py`:

```python
def test_package_imports():
    import live_ai_brain

    assert live_ai_brain.__doc__
```

- [ ] **Step 3: Run test to verify scaffold**

Run: `python -m pytest tests/test_scaffold.py -v`

Expected: one passing test.

- [ ] **Step 4: Commit**

```bash
git add pyproject.toml src/live_ai_brain/__init__.py data/.gitkeep tests/test_scaffold.py
git commit -m "chore: scaffold live commerce ai brain app"
```

## Task 2: Domain Models and JSON Storage

**Files:**
- Create: `src/live_ai_brain/models.py`
- Create: `src/live_ai_brain/storage.py`
- Create: `tests/test_storage.py`

- [ ] **Step 1: Write failing storage test**

Create `tests/test_storage.py`:

```python
from pathlib import Path

from live_ai_brain.models import ExecutionTask, TaskStatus
from live_ai_brain.storage import JsonStore


def test_json_store_round_trips_execution_tasks(tmp_path: Path):
    store = JsonStore(tmp_path)
    task = ExecutionTask(
        id="task-1",
        session_id="session-1",
        owner_role="主播",
        title="改开场痛点话术",
        detail="把文言文痛点前置到前 20 秒。",
        status=TaskStatus.ADOPTED,
    )

    store.save_tasks([task])
    loaded = store.load_tasks()

    assert loaded == [task]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_storage.py -v`

Expected: FAIL because `live_ai_brain.models` does not exist.

- [ ] **Step 3: Implement models**

Create `src/live_ai_brain/models.py`:

```python
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
```

- [ ] **Step 4: Implement JSON storage**

Create `src/live_ai_brain/storage.py`:

```python
from __future__ import annotations

import json
from pathlib import Path

from live_ai_brain.models import ExecutionTask


class JsonStore:
    def __init__(self, root: Path | str = "data") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    @property
    def tasks_path(self) -> Path:
        return self.root / "execution_tasks.json"

    def save_tasks(self, tasks: list[ExecutionTask]) -> None:
        payload = [task.to_dict() for task in tasks]
        self.tasks_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def load_tasks(self) -> list[ExecutionTask]:
        if not self.tasks_path.exists():
            return []
        payload = json.loads(self.tasks_path.read_text(encoding="utf-8"))
        return [ExecutionTask.from_dict(item) for item in payload]
```

- [ ] **Step 5: Run test to verify it passes**

Run: `python -m pytest tests/test_storage.py -v`

Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add src/live_ai_brain/models.py src/live_ai_brain/storage.py tests/test_storage.py
git commit -m "feat: add domain models and json storage"
```

## Task 3: Product Knowledge Loader

**Files:**
- Create: `src/live_ai_brain/knowledge.py`
- Create: `tests/test_knowledge.py`

- [ ] **Step 1: Write failing knowledge test**

Create `tests/test_knowledge.py`:

```python
from pathlib import Path

from live_ai_brain.knowledge import KnowledgeBase


def test_knowledge_base_loads_markdown_and_retrieves_matching_chunks(tmp_path: Path):
    product_dir = tmp_path / "窦神文言文速通"
    product_dir.mkdir()
    (product_dir / "04-核心卖点.md").write_text(
        "# 核心卖点\n课程围绕小石潭记和岳阳楼记建立文言文方法。",
        encoding="utf-8",
    )
    (product_dir / "13-成交转化话术.md").write_text(
        "# 成交话术\n家长拍下后注意查收豆神短信。",
        encoding="utf-8",
    )

    kb = KnowledgeBase.from_product_dir(product_dir)
    results = kb.search("岳阳楼记 方法", limit=1)

    assert results[0].source.endswith("04-核心卖点.md")
    assert "岳阳楼记" in results[0].text
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_knowledge.py -v`

Expected: FAIL because `KnowledgeBase` is missing.

- [ ] **Step 3: Implement knowledge loader**

Create `src/live_ai_brain/knowledge.py`:

```python
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class KnowledgeChunk:
    source: str
    text: str


class KnowledgeBase:
    def __init__(self, chunks: list[KnowledgeChunk]) -> None:
        self.chunks = chunks

    @classmethod
    def from_product_dir(cls, product_dir: Path | str) -> "KnowledgeBase":
        root = Path(product_dir)
        chunks: list[KnowledgeChunk] = []
        for path in sorted(root.rglob("*")):
            if path.suffix.lower() not in {".md", ".txt"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore").strip()
            if text:
                chunks.append(KnowledgeChunk(source=str(path), text=text))
        return cls(chunks)

    def search(self, query: str, limit: int = 5) -> list[KnowledgeChunk]:
        terms = [term for term in query.strip().split() if term]
        scored: list[tuple[int, KnowledgeChunk]] = []
        for chunk in self.chunks:
            haystack = chunk.text.lower()
            score = sum(haystack.count(term.lower()) for term in terms)
            if score > 0:
                scored.append((score, chunk))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [chunk for _, chunk in scored[:limit]]
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_knowledge.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/live_ai_brain/knowledge.py tests/test_knowledge.py
git commit -m "feat: load product knowledge files"
```

## Task 4: Data Ingestion

**Files:**
- Create: `src/live_ai_brain/ingest.py`
- Create: `tests/test_ingest.py`

- [ ] **Step 1: Write failing ingestion test**

Create `tests/test_ingest.py`:

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_ingest.py -v`

Expected: FAIL because `parse_live_metrics_csv` is missing.

- [ ] **Step 3: Implement CSV parser**

Create `src/live_ai_brain/ingest.py`:

```python
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
```

- [ ] **Step 4: Run ingestion test**

Run: `python -m pytest tests/test_ingest.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/live_ai_brain/ingest.py tests/test_ingest.py
git commit -m "feat: parse live and qianchuan metrics"
```

## Task 5: Compliance and Replay Logic

**Files:**
- Create: `src/live_ai_brain/compliance.py`
- Create: `src/live_ai_brain/replay.py`
- Create: `tests/test_compliance.py`
- Create: `tests/test_replay.py`

- [ ] **Step 1: Write failing compliance test**

Create `tests/test_compliance.py`:

```python
from live_ai_brain.compliance import check_compliance


def test_check_compliance_flags_absolute_learning_claims():
    report = check_compliance("这套课保证提分，孩子一定有效。")

    assert report.risks[0].category == "效果承诺风险"
    assert "帮助孩子建立方法" in report.risks[0].safer_rewrite
```

- [ ] **Step 2: Write failing replay test**

Create `tests/test_replay.py`:

```python
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
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `python -m pytest tests/test_compliance.py tests/test_replay.py -v`

Expected: FAIL because modules are missing.

- [ ] **Step 4: Implement compliance**

Create `src/live_ai_brain/compliance.py`:

```python
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ComplianceRisk:
    category: str
    phrase: str
    reason: str
    safer_rewrite: str


@dataclass(frozen=True)
class ComplianceReport:
    risks: list[ComplianceRisk]

    @property
    def passed(self) -> bool:
        return not self.risks


RISKY_PHRASES = {
    "保证提分": "效果承诺风险",
    "一定有效": "效果承诺风险",
    "稳拿分": "效果承诺风险",
    "永久有效": "权益时效风险",
    "无理由退款": "售后口径风险",
}


def check_compliance(text: str) -> ComplianceReport:
    risks: list[ComplianceRisk] = []
    for phrase, category in RISKY_PHRASES.items():
        if phrase in text:
            risks.append(
                ComplianceRisk(
                    category=category,
                    phrase=phrase,
                    reason="该表达可能构成绝对化承诺或与当前官方口径不一致。",
                    safer_rewrite="建议改为：帮助孩子建立方法、提升理解能力，具体效果因孩子基础和学习投入而异。",
                )
            )
    return ComplianceReport(risks=risks)
```

- [ ] **Step 5: Implement replay report**

Create `src/live_ai_brain/replay.py`:

```python
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

    if click_rate < 0.05:
        diagnoses.append("商品点击偏弱：用户进入后没有被充分引导点击商品。")
        actions.append("强化贴片和场控提醒，在讲到权益和下单流程时明确引导点击商品。")
    if order_rate < 0.15:
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
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `python -m pytest tests/test_compliance.py tests/test_replay.py -v`

Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add src/live_ai_brain/compliance.py src/live_ai_brain/replay.py tests/test_compliance.py tests/test_replay.py
git commit -m "feat: add compliance and replay diagnosis"
```

## Task 6: Content Draft Generator

**Files:**
- Create: `src/live_ai_brain/content.py`
- Create: `tests/test_content.py`

- [ ] **Step 1: Write failing content test**

Create `tests/test_content.py`:

```python
from live_ai_brain.content import generate_live_script_pack


def test_generate_live_script_pack_includes_required_sections():
    pack = generate_live_script_pack(
        product_name="窦神文言文速通",
        pain_point="孩子文言文翻译靠猜",
        benefit="直播课+纸质资料+服务老师跟进",
    )

    assert "开场留人" in pack
    assert "异议处理" in pack
    assert "成交转化" in pack
    assert "保证提分" not in pack
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python -m pytest tests/test_content.py -v`

Expected: FAIL because module is missing.

- [ ] **Step 3: Implement deterministic draft generator**

Create `src/live_ai_brain/content.py`:

```python
from __future__ import annotations


def generate_live_script_pack(product_name: str, pain_point: str, benefit: str) -> str:
    return f"""# {product_name} 主播话术包

## 开场留人
各位家长，如果孩子现在{pain_point}，先别急着怪孩子不努力，很多时候是文言文学习方法还没有搭起来。

## 痛点放大
孩子只会背课文，但换一篇课外文言文就不会翻译、不会抓关键词、不会判断文章主旨，这说明需要补的是方法。

## 产品解释
{product_name} 会围绕经典篇目，帮助孩子梳理作者背景、文本理解、字词句式、翻译方法和常见题型。

## 异议处理
如果家长担心孩子基础薄弱，可以先看孩子是否存在读不懂、翻译靠猜、答题没思路的问题。这类孩子更需要系统方法。

## 成交转化
需要的家长可以根据孩子年级选择对应规格。下单后注意查收短信，按服务老师提示领取课程和资料。当前权益以商品页为准：{benefit}。

## 合规提醒
不要承诺保证提分、一定有效、永久有效；表达重点放在建立方法、提升理解能力和规范学习路径。
"""


def generate_short_video_script(product_name: str, pain_point: str) -> str:
    return f"""# {product_name} 短视频脚本

## 前 3 秒钩子
孩子文言文总是靠猜，不一定是笨，可能是方法没搭起来。

## 痛点场景
一到翻译题就卡住，背过的课文会，换一篇课外文言文就没思路。

## 产品植入
{product_name} 从经典篇目入手，带孩子学作者背景、重点字词、翻译方法和答题思路。

## 结尾行动
如果孩子{pain_point}，可以先把文言文学习方法补起来。
"""


def generate_overlay_copy(product_name: str, benefit: str) -> str:
    return f"""# {product_name} 贴片 / KT 板文案

主标题：文言文读不懂，先补方法

核心卖点：
1. 经典篇目带方法
2. 翻译、理解、答题一起梳理
3. 适合需要系统补文言文方法的孩子

权益提醒：{benefit}

下单提醒：拍下后注意查收短信，按服务老师提示完成领取。
"""
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python -m pytest tests/test_content.py -v`

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/live_ai_brain/content.py tests/test_content.py
git commit -m "feat: generate structured content drafts"
```

## Task 7: Streamlit MVP App

**Files:**
- Create: `src/live_ai_brain/app.py`
- Create: `README.md` modification

- [ ] **Step 1: Create Streamlit app**

Create `src/live_ai_brain/app.py`:

```python
from __future__ import annotations

from pathlib import Path

import streamlit as st

from live_ai_brain.compliance import check_compliance
from live_ai_brain.content import (
    generate_live_script_pack,
    generate_overlay_copy,
    generate_short_video_script,
)
from live_ai_brain.ingest import parse_live_metrics_csv, parse_qianchuan_metrics_csv
from live_ai_brain.knowledge import KnowledgeBase
from live_ai_brain.replay import build_replay_report


PRODUCT_ROOT = Path("products") / "窦神文言文速通"


def main() -> None:
    st.set_page_config(page_title="电商直播 AI 大脑 C-lite", layout="wide")
    st.title("电商直播 AI 大脑 C-lite")
    st.caption("第一版：数据导入、AI 复盘、内容生成、执行清单、合规检查")

    tab_upload, tab_replay, tab_content, tab_compliance = st.tabs(
        ["数据导入", "AI 复盘", "内容工厂", "合规检查"]
    )

    with tab_upload:
        st.subheader("数据和素材来源")
        st.text_input("飞书表格链接", placeholder="粘贴飞书在线表格链接，第一版用于来源记录")
        st.text_input("百度网盘分享链接", placeholder="粘贴网盘链接，关键素材下载后再上传")
        st.text_input("百度网盘提取码", placeholder="如有提取码，填写在这里")
        st.file_uploader("上传直播数据表 CSV/XLSX", type=["csv", "xlsx"])
        st.file_uploader("上传千川数据表 CSV/XLSX", type=["csv", "xlsx"])
        st.file_uploader("上传录屏/成片/图片素材", type=["mp4", "mov", "png", "jpg", "jpeg"])

    with tab_replay:
        st.subheader("AI 复盘")
        live_file = st.file_uploader("直播数据表", type=["csv", "xlsx"], key="live")
        qc_file = st.file_uploader("千川数据表", type=["csv", "xlsx"], key="qc")
        if live_file and qc_file and st.button("生成复盘报告"):
            tmp_dir = Path("data") / "uploads"
            tmp_dir.mkdir(parents=True, exist_ok=True)
            live_path = tmp_dir / live_file.name
            qc_path = tmp_dir / qc_file.name
            live_path.write_bytes(live_file.getbuffer())
            qc_path.write_bytes(qc_file.getbuffer())
            report = build_replay_report(
                parse_live_metrics_csv(live_path),
                parse_qianchuan_metrics_csv(qc_path),
            )
            st.markdown("### 核心结论")
            st.write(report.summary)
            st.markdown("### 问题诊断")
            st.write(report.diagnoses)
            st.markdown("### 下一场动作")
            st.write(report.next_actions)

    with tab_content:
        st.subheader("内容工厂")
        product_name = st.text_input("产品名称", value="窦神文言文速通")
        pain_point = st.text_input("主推痛点", value="孩子文言文翻译靠猜")
        benefit = st.text_input("当前权益", value="直播课+纸质资料+服务老师跟进")
        if st.button("生成直播话术"):
            st.markdown(generate_live_script_pack(product_name, pain_point, benefit))
        if st.button("生成短视频脚本"):
            st.markdown(generate_short_video_script(product_name, pain_point))
        if st.button("生成贴片/KT 板文案"):
            st.markdown(generate_overlay_copy(product_name, benefit))

    with tab_compliance:
        st.subheader("合规检查")
        text = st.text_area("粘贴话术、脚本或贴片文案")
        if st.button("检查风险"):
            report = check_compliance(text)
            if report.passed:
                st.success("未发现内置规则命中的风险表达。")
            else:
                for risk in report.risks:
                    st.error(f"{risk.category}：{risk.phrase}")
                    st.write(risk.reason)
                    st.info(risk.safer_rewrite)

        if PRODUCT_ROOT.exists():
            kb = KnowledgeBase.from_product_dir(PRODUCT_ROOT)
            st.caption(f"已加载产品知识片段：{len(kb.chunks)}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Update README run instructions**

Replace the first-stage section in `README.md` with:

```markdown
## 第一阶段 MVP

本地运行：

```powershell
python -m pip install -e ".[dev]"
python -m streamlit run src/live_ai_brain/app.py
```

第一版支持：

- 本地上传直播数据表和千川数据表
- 登记飞书表格链接和百度网盘素材链接
- 生成直播复盘报告
- 生成主播话术、短视频脚本、贴片/KT板文案
- 检查常见合规风险表达
```
```

- [ ] **Step 3: Run unit tests**

Run: `python -m pytest -v`

Expected: all tests pass.

- [ ] **Step 4: Run app smoke test**

Run: `python -m streamlit run src/live_ai_brain/app.py`

Expected: Streamlit prints a local URL and the app loads with tabs `数据导入`, `AI 复盘`, `内容工厂`, `合规检查`.

- [ ] **Step 5: Commit**

```bash
git add src/live_ai_brain/app.py README.md
git commit -m "feat: add streamlit c-lite mvp"
```

## Task 8: End-to-End Fixture and Verification

**Files:**
- Create: `tests/fixtures/live_metrics.csv`
- Create: `tests/fixtures/qianchuan_metrics.csv`
- Create: `tests/test_end_to_end.py`

- [ ] **Step 1: Add fixture data**

Create `tests/fixtures/live_metrics.csv`:

```csv
产品名称,直播日期,直播时段,主播,场控,活动价格,权益,进入人数,平均停留秒,互动数,商品点击,成交数,成交额
窦神文言文速通,2026-06-01,19:00-21:00,主播A,场控B,199,直播课+纸质资料,1000,45,200,20,2,398
```

Create `tests/fixtures/qianchuan_metrics.csv`:

```csv
消耗,点击率,转化率,ROI,成交成本,主投素材
800,0.8,0.1,0.5,400,文言文痛点口播
```

- [ ] **Step 2: Add end-to-end test**

Create `tests/test_end_to_end.py`:

```python
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
```

- [ ] **Step 3: Run full verification**

Run: `python -m pytest -v`

Expected: all tests pass.

- [ ] **Step 4: Commit**

```bash
git add tests/fixtures/live_metrics.csv tests/fixtures/qianchuan_metrics.csv tests/test_end_to_end.py
git commit -m "test: add end-to-end replay fixture"
```

## Self-Review

- Spec coverage: upload flow is covered by Tasks 4 and 7; knowledge and口径 are covered by Task 3 and Task 7; replay diagnosis by Task 5; content generation by Task 6; compliance by Task 5; execution task storage foundation by Task 2; end-to-end verification by Task 8.
- Known deferral: real Feishu sync, Baidu download, video transcription, OpenAI provider calls, auth, and multi-user workflow are intentionally out of scope for this MVP plan and listed as second-stage work in the approved design.
- Placeholder scan: no unfinished markers or vague implementation steps remain.
- Type consistency: `LiveMetrics`, `QianchuanMetrics`, `ExecutionTask`, `TaskStatus`, `ReplayReport`, and generator function names are introduced before use and reused consistently.

from __future__ import annotations

import re
from pathlib import Path, PurePosixPath
from uuid import uuid4

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


UPLOAD_DIR = Path("data") / "uploads"
_SAFE_FILENAME_RE = re.compile(r"[^A-Za-z0-9._-]+")
PRODUCT_DIR = Path("products") / "窦神文言文速通"


def _save_uploaded_file(uploaded_file: st.runtime.uploaded_file_manager.UploadedFile) -> Path:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    raw_name = str(uploaded_file.name or "upload")
    base_name = PurePosixPath(raw_name.replace("\\", "/")).name
    source_path = Path(base_name)
    suffix = _SAFE_FILENAME_RE.sub("", source_path.suffix)[:16]
    stem = _SAFE_FILENAME_RE.sub("_", source_path.stem).strip("._-") or "upload"
    target = UPLOAD_DIR / f"{stem[:80]}_{uuid4().hex[:12]}{suffix}"
    upload_root = UPLOAD_DIR.resolve()
    if not target.resolve().is_relative_to(upload_root):
        raise ValueError("Unsafe upload filename")
    target.write_bytes(uploaded_file.getbuffer())
    return target


def _show_replay_error(exc: Exception, *, expected_data_error: bool) -> None:
    if expected_data_error:
        st.error("无法生成复盘：请检查上传的数据文件是否正确，表头、字段和数字格式需要与模板一致。")
    else:
        st.error("无法生成复盘：系统处理时遇到问题，请稍后重试或联系技术同事。")
    with st.expander("技术细节"):
        st.caption(f"{type(exc).__name__}: {exc}")


def _show_markdown_list(items: list[str]) -> None:
    for item in items:
        st.markdown(f"- {item}")


def main() -> None:
    st.set_page_config(page_title="电商直播 AI 大脑 C-lite", layout="wide")
    st.title("电商直播 AI 大脑 C-lite")
    st.caption("第一版：数据导入、AI 复盘、内容生成、执行清单、合规检查.")

    if PRODUCT_DIR.exists():
        knowledge_base = KnowledgeBase.from_product_dir(PRODUCT_DIR)
        st.info(f"已加载产品知识库：{len(knowledge_base.chunks)} 个资料片段")

    data_tab, replay_tab, content_tab, compliance_tab = st.tabs(
        ["数据导入", "AI 复盘", "内容工厂", "合规检查"]
    )

    with data_tab:
        st.text_input("飞书表格链接")
        st.text_input("百度网盘分享链接")
        st.text_input("百度网盘提取码")
        st.file_uploader("直播数据表", type=["csv", "xlsx", "xls"])
        st.file_uploader("千川数据表", type=["csv", "xlsx", "xls"])
        st.file_uploader(
            "录屏/成片/图片素材",
            accept_multiple_files=True,
            type=["mp4", "mov", "avi", "mkv", "jpg", "jpeg", "png", "webp"],
        )

    with replay_tab:
        live_file = st.file_uploader("上传直播数据表", type=["csv", "xlsx", "xls"], key="replay_live")
        qianchuan_file = st.file_uploader(
            "上传千川数据表", type=["csv", "xlsx", "xls"], key="replay_qianchuan"
        )
        if live_file and qianchuan_file:
            try:
                live_path = _save_uploaded_file(live_file)
                qianchuan_path = _save_uploaded_file(qianchuan_file)
                live_metrics = parse_live_metrics_csv(live_path)
                qianchuan_metrics = parse_qianchuan_metrics_csv(qianchuan_path)
                report = build_replay_report(live_metrics, qianchuan_metrics)

                st.subheader("核心结论")
                st.write(report.summary)
                st.subheader("问题诊断")
                _show_markdown_list(report.diagnoses)
                st.subheader("下一场动作")
                _show_markdown_list(report.next_actions)
            except (ValueError, KeyError, TypeError, UnicodeDecodeError) as exc:
                _show_replay_error(exc, expected_data_error=True)
            except Exception as exc:  # pragma: no cover - Streamlit UI guard
                _show_replay_error(exc, expected_data_error=False)
        else:
            st.info("请上传直播数据表和千川数据表，系统会自动保存到 data/uploads 并生成复盘。")

    with content_tab:
        product_name = st.text_input("产品名称", value="窦神文言文速通")
        pain_point = st.text_input("用户痛点", value="孩子文言文翻译靠猜")
        benefit = st.text_input("权益卖点", value="直播课+纸质资料+服务老师跟进")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("生成直播话术"):
                st.markdown(generate_live_script_pack(product_name, pain_point, benefit))
        with col2:
            if st.button("生成短视频脚本"):
                st.markdown(generate_short_video_script(product_name, pain_point))
        with col3:
            if st.button("生成贴片/KT 板文案"):
                st.markdown(generate_overlay_copy(product_name, benefit))

    with compliance_tab:
        text = st.text_area("待检查文案", height=220)
        if st.button("检查合规风险"):
            report = check_compliance(text)
            if report.passed:
                st.success("未发现常见合规风险表达。")
            else:
                st.error("发现合规风险，请调整后再使用。")
                for risk in report.risks:
                    with st.expander(f"{risk.category}：{risk.phrase}", expanded=True):
                        st.write(risk.reason)
                        st.write(risk.safer_rewrite)


if __name__ == "__main__":
    main()

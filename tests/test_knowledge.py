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

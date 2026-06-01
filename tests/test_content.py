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

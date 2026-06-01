from live_ai_brain.content import (
    generate_live_script_pack,
    generate_overlay_copy,
    generate_short_video_script,
)


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


def test_generate_short_video_script_includes_required_sections_and_product():
    script = generate_short_video_script(
        product_name="窦神文言文速通",
        pain_point="孩子文言文翻译靠猜",
    )

    assert "短视频脚本" in script
    assert "前 3 秒钩子" in script
    assert "产品植入" in script
    assert "窦神文言文速通" in script
    assert "保证提分" not in script


def test_generate_overlay_copy_includes_required_sections_and_benefit():
    copy = generate_overlay_copy(
        product_name="窦神文言文速通",
        benefit="直播课+纸质资料+服务老师跟进",
    )

    assert "贴片 / KT 板文案" in copy
    assert "主标题" in copy
    assert "权益提醒" in copy
    assert "直播课+纸质资料+服务老师跟进" in copy
    assert "保证提分" not in copy

from live_ai_brain.compliance import check_compliance


def test_check_compliance_flags_absolute_learning_claims():
    report = check_compliance("这套课保证提分，孩子一定有效。")

    assert report.risks[0].category == "效果承诺风险"
    assert "帮助孩子建立方法" in report.risks[0].safer_rewrite

from live_ai_brain.compliance import check_compliance


def test_check_compliance_flags_absolute_learning_claims():
    report = check_compliance("这套课保证提分，孩子一定有效。")

    assert report.risks[0].category == "效果承诺风险"
    assert "帮助孩子建立方法" in report.risks[0].safer_rewrite


def test_check_compliance_passes_clean_text():
    report = check_compliance("这套课会帮助孩子梳理方法，具体学习效果因基础和投入而异。")

    assert report.passed
    assert report.risks == []


def test_check_compliance_detects_multiple_risky_phrases():
    report = check_compliance("这套课保证提分，还能稳拿分。")

    assert [risk.phrase for risk in report.risks] == ["保证提分", "稳拿分"]
    assert all(risk.category == "效果承诺风险" for risk in report.risks)
    assert not report.passed


def test_check_compliance_flags_non_effect_categories():
    report = check_compliance("权益永久有效，支持无理由退款。")

    categories = {risk.category for risk in report.risks}
    assert categories == {"权益时效风险", "售后口径风险"}

import pytest
from biascheck import BaseCheck

def test_basecheck_initialization(basecheck):
    assert isinstance(basecheck, BaseCheck)

def test_basecheck_analyze_text(basecheck, sample_text):
    result = basecheck.analyze(sample_text)
    assert isinstance(result, dict)
    assert "bias_score" in result
    assert "bias_categories" in result

def test_basecheck_analyze_empty_text(basecheck):
    result = basecheck.analyze("")
    assert isinstance(result, dict)
    assert "error" in result 
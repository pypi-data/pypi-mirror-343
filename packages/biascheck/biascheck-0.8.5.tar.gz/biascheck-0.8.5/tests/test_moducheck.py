import pytest
from biascheck import ModuCheck

def test_moducheck_initialization(moducheck):
    assert isinstance(moducheck, ModuCheck)

def test_moducheck_analyze_model(moducheck):
    # Test with a simple model name that should be recognized
    result = moducheck.analyze("gpt2")
    assert isinstance(result, dict)
    assert "bias_score" in result
    assert "bias_categories" in result

def test_moducheck_analyze_invalid_model(moducheck):
    # Test with an invalid model name
    result = moducheck.analyze("invalid_model_name")
    assert isinstance(result, dict)
    assert "error" in result 
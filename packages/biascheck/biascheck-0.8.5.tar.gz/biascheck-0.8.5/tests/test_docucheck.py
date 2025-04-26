import pytest
from biascheck import DocuCheck

def test_docucheck_initialization():
    analyzer = DocuCheck(terms=["lazy", "unreliable"])
    assert analyzer.terms == ["lazy", "unreliable"]
    assert analyzer.bias_threshold > 0

def test_docucheck_analyze_biased_text(docucheck, sample_text):
    result = docucheck.analyze(sample_text)
    assert "similarity" in result
    assert result["similarity"] >= docucheck.bias_threshold

def test_docucheck_analyze_neutral_text(docucheck):
    neutral_text = "The individual completed the task efficiently."
    result = docucheck.analyze(neutral_text)
    assert "similarity" in result
    assert result["similarity"] < docucheck.bias_threshold 
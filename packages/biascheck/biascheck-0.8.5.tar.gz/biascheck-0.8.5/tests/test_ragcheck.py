import pytest
from biascheck import RAGCheck

def test_ragcheck_initialization(ragcheck):
    assert isinstance(ragcheck, RAGCheck)

def test_ragcheck_analyze_rag_system(ragcheck):
    # Test with a simple RAG system configuration
    config = {
        "retriever": "simple",
        "generator": "gpt2",
        "documents": ["Sample document 1", "Sample document 2"]
    }
    result = ragcheck.analyze(config)
    assert isinstance(result, dict)
    assert "bias_score" in result
    assert "bias_categories" in result

def test_ragcheck_analyze_invalid_config(ragcheck):
    # Test with an invalid configuration
    result = ragcheck.analyze({})
    assert isinstance(result, dict)
    assert "error" in result 
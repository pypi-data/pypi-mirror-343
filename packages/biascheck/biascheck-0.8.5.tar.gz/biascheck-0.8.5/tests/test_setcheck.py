import pytest
import pandas as pd
from biascheck import SetCheck

def test_setcheck_initialization(setcheck):
    assert isinstance(setcheck, SetCheck)

def test_setcheck_analyze_biased_data(setcheck, sample_df):
    result = setcheck.analyze()
    assert isinstance(result, pd.DataFrame)
    assert 'similarity' in result.columns
    assert 'flagged' in result.columns
    assert 'sentiment' in result.columns
    assert 'sentiment_score' in result.columns
    assert result.loc[0, 'similarity'] > result.loc[1, 'similarity']
    assert result.loc[0, 'flagged'] is True
    assert result.loc[1, 'flagged'] is False

def test_setcheck_analyze_empty_dataframe(setcheck):
    empty_df = pd.DataFrame(columns=['text'])
    setcheck.data = empty_df
    setcheck.input_cols = ['text']
    result = setcheck.analyze()
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0

def test_setcheck_with_contextual_analysis():
    df = pd.DataFrame({
        'text': ['That person is lazy and unreliable.', 'The individual completed the task efficiently.'],
        'label': ['biased', 'neutral']
    })
    setcheck = SetCheck(
        data=df,
        input_cols=['text'],
        terms=['lazy', 'unreliable'],
        use_contextual_analysis=True,
        similarity_threshold=0.5
    )
    result = setcheck.analyze()
    assert 'This sentence promotes discrimination.' in result.columns
    assert 'This sentence is fair and unbiased.' in result.columns
    assert 'This sentence is offensive.' in result.columns
    assert 'final_contextual_analysis' in result.columns 
_author_ = "Harshit Pandey"

import torch
import pytest
from decepticonlp.metrics import temporal_metrics
import gensim.downloader as api

model_gigaword = api.load("glove-wiki-gigaword-100")
def sentenceToTensor(text):
    op = torch.zeros((len(text.split(' ')),model_gigaword['i'].shape[0]))
    for i,word in enumerate(text.split(' ')):
        op[i] = torch.from_numpy(model_gigaword[word])
    return op

@pytest.mark.parametrize(
    "text,expected_result",
    [
        (
            "i like dogs",
            torch.tensor([[1.1921e-07],
                        [2.2054e-05],
                        [8.4886e-01]])
        ),
        (
            "he ran across the street",
            torch.tensor([[1.7881e-07],
                        [3.6359e-06],
                        [3.8207e-05],
                        [1.5679e-01],
                        [9.7338e-01]])

        )
    ],
)
def test_temporal_score(text,expected_result):
    torch.manual_seed(99)
    text = sentenceToTensor(text)
    assert torch.isclose(
        temporal_metrics.temporal_score(text),rtol = 1e-4
    )
    
@pytest.mark.parametrize(
    "text,expected_result",
    [
        (
            "i like dogs",
            torch.tensor([[5.9605e-08],
                        [1.9789e-05],
                        [0.0000e+00]])

        ),
        (
            "he ran across the street",
            torch.tensor([[1.7881e-07],
                        [4.3511e-06],
                        [1.8537e-05],
                        [1.1431e-01],
                        [0.0000e+00]])

        )
    ],
)
def test_tailed_temporal_score(text,expected_result):
    torch.manual_seed(99)
    text = sentenceToTensor(text)
    assert torch.isclose(
        temporal_metrics.temportal_tail_score(text),rtol = 1e-4
    )

@pytest.mark.parametrize(
    "text,lambda_,expected_result",
    [
        (
            "i like dogs",
            0.5,
            torch.tensor([[6.8545e-07],
                        [3.8507e-03],
                        [8.4886e-01]])
        ),
        (
            "he ran across the street",
            0.5,
            torch.tensor([[1.7881e-07],
                            [3.6359e-06],
                            [3.8207e-05],
                            [1.5730e-01],
                            [9.7338e-01]])
        )
    ],
)
def test_combined_temporal_score(text,lambda_,expected_result):
    torch.manual_seed(99)
    text = sentenceToTensor(text)
    assert torch.isclose(
        temporal_metrics.combined_temporal_score(text,lambda_),rtol = 1e-4
    )

_author_ = "Harshit Pandey"

import torch
import pytest
from decepticonlp.metrics import temporal_metrics


@pytest.mark.parametrize(
    "text,expected_result",
    [
        (
            "good",
            torch.tensor([  [0.0882],
                            [0.3892],
                            [0.2367],
                            [0.7079]])
        ),
        (
            "!@#$%^&*(",
            torch.tensor([   [0.0600],
                            [0.0541],
                            [0.1060],
                            [0.0981],
                            [0.1669],
                            [0.1649],
                            [0.2615],
                            [0.2729],
                            [0.4328]])
        )
    ],
)
def test_temporal_score(text,expected_result):
    torch.manual_seed(98)
    assert torch.isclose(
        temporal_metrics.temporal_score(text),rtol = 1e-4
    )
    
@pytest.mark.parametrize(
    "text,expected_result",
    [
        (
            "good",
            torch.tensor([  [0.2703],
                            [0.4244],
                            [0.4688],
                            [0.0000]])
        ),
        (
            "!@#$%^&*(",
            torch.tensor([   [0.1171],
                            [0.1435],
                            [0.1787],
                            [0.2188],
                            [0.2747],
                            [0.3365],
                            [0.4296],
                            [0.5286],
                            [0.0000]])
        )
    ],
)
def test_tailed_temporal_score(text,expected_result):
    torch.manual_seed(98)
    assert torch.isclose(
        temporal_metrics.combined_temporal_score(text),rtol = 1e-4
    )

@pytest.mark.parametrize(
    "text,lambda_,expected_result",
    [
        (
            "good",
            0.5,
            torch.tensor([  [2.5064e-05],
                            [1.2832e-03],
                            [3.7908e-02],
                            [1.3923e-01]])
        ),
        (
            "!@#$%^&*(",
            0.5,
            torch.tensor([  [2.4140e-06],
                            [9.7603e-06],
                            [3.9652e-05],
                            [1.6111e-04],
                            [6.5784e-04],
                            [2.7144e-03],
                            [1.1449e-02],
                            [5.0346e-02],
                            [7.7066e-02]])
        )
    ],
)
def test_combined_temporal_score(text,lambda_,expected_result):
    torch.manual_seed(99)
    assert torch.isclose(
        temporal_metrics.combined_temporal_score(text,lambda_),rtol = 1e-4
    )

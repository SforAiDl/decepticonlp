_author_ = "Somesh Singh"

import random

import pytest

from decepticonlp.metrics import char_metrics


@pytest.mark.parametrize(
    "text1, text2, expected_result",
    [("Word", "Wordy", 1), ("Word", "Wrod", 2), ("H", "H", 0)],
)
def test_levenshtein(text1, text2, expected_result):
    levenshtein_distance = char_metrics.Levenshtein()
    assert levenshtein_distance.calculate(text1, text2) == expected_result


@pytest.mark.parametrize(
    "text1, text2, expected_result",
    [("Word", "Wordy", 0.1111111111111111), ("Word", "Wrod", 0.25), ("H", "H", 0)],
)
def test_levenshtein_sum(text1, text2, expected_result):
    levenshtein_distance = char_metrics.Levenshtein()
    err = levenshtein_distance.calculate(text1, text2, "sum") - expected_result
    assert -1e-5 < err < 1e-5


@pytest.mark.parametrize(
    "text1, text2, expected_result",
    [("Word", "Wordy", 0.2), ("Word", "Wrod", 0.5), ("H", "H", 0)],
)
def test_levenshtein_lcs(text1, text2, expected_result):
    levenshtein_distance = char_metrics.Levenshtein()
    err = levenshtein_distance.calculate(text1, text2, "lcs") - expected_result
    assert -1e-5 < err < 1e-5


@pytest.mark.parametrize(
    "text1, text2, expected_result",
    [
        ("Word", "Wordy", 1.4142135623730951),
        ("Word was", "Word is that", 1.7320508075688772),
        ("H", "H", 0),
    ],
)
def test_euclid(text1, text2, expected_result):
    euclidean_distance = char_metrics.Euclidean()
    err = euclidean_distance.calculate(text1, text2) - expected_result
    assert -1e-5 < err < 1e-5


@pytest.mark.parametrize(
    "text1, text2, expected_result",
    [
        ("Word", "Wordy", 1),
        ("Word was", "Word is that", 0.8660254037844386),
        ("H", "H", 0),
    ],
)
def test_euclid_norm(text1, text2, expected_result):
    euclidean_distance = char_metrics.Euclidean()
    err = euclidean_distance.calculate(text1, text2, norm=True) - expected_result
    assert -1e-5 < err < 1e-5


@pytest.mark.parametrize(
    "text1, text2, expected_result",
    [
        ("Word", "Wordy", 0.19999999999999996),
        ("Word", "Wrod", 0),
        ("Word was", "Word is that", 0.36363636363636365),
    ],
)
def test_jaccard(text1, text2, expected_result):
    jaccard_similarity = char_metrics.Jaccard()
    err = jaccard_similarity.calculate(text1, text2) - expected_result
    assert -1e-5 < err < 1e-5


@pytest.mark.parametrize(
    "text1, text2, window, expected_result",
    [
        ("Word", "Wordy", 1, 0.19999999999999996),
        ("Word", "Wordy", 2, 0.25),
        ("Word", "Wordy", 3, 0.33333333333333337),
        ("Word", "Wordy", 10, 0.19999999999999996),
    ],
)
def test_jaccard_window(text1, text2, window, expected_result):
    jaccard_similarity = char_metrics.Jaccard()
    err = jaccard_similarity.calculate(text1, text2, ngrams=window) - expected_result
    assert -1e-5 < err < 1e-5


def test_jaccard_with_short_length():
    with pytest.raises(AssertionError):
        jaccard_similarity = char_metrics.Jaccard()
        jaccard_similarity.calculate("Word", "Wordy", ngrams=10, ignore=False)

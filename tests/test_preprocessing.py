import random

import pytest

from decepticonlp.preprocessing import preprocessing

import math


@pytest.mark.parametrize(
    "text1, expected_result",
    [
        ("Dinosaurs were killed by asteroids", "dinosaur were kill by asteroid"),
        ("Adversarial Library", "adversari librari"),
    ],
)
def test_stemmer_default(text1, text2, expected_result):
    stem = preprocessing.Stem()
    assert stem.apply(text1) == expected_result


@pytest.mark.parametrize(
    "text1, expected_result",
    [
        ("Dinosaurs were killed by asteroids", "dinosa wer kil by asteroid"),
        ("Adversarial Library", "advers libr"),
    ],
)
def test_stemmer_lancaster(text1, text2, expected_result):
    stem = preprocessing.Stem()
    assert stem.apply(text1, type="lancaster") == expected_result

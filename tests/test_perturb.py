_author_ = "Rohit Patil"

import random

import pytest

from decepticonlp.transforms import perturb


@pytest.mark.parametrize(
    "word, expected_result",
    [
        ("Bob", "Bb"),
        ("Never odd or even", "Never odd o even"),
        ("Do geese see God?", "Do geese se God?"),
        ("Elon Musk names his kid.", "Elon Musk names his kd."),
    ],
)
def test_perturb_delete(word, expected_result):
    random.seed(42)
    assert perturb.delete(word) == expected_result


def test_perturb_delete_with_character_size_less_than_three():
    with pytest.raises(AssertionError):
        perturb.delete("To")

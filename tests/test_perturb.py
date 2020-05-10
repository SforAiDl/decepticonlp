_author_ = "Rohit Patil"

import random

import pytest

from decepticonlp.transforms import perturb


@pytest.mark.parametrize(
    "word, expected_result", [("Bob", "Bb"), ("Hey there", "Hey there"), ("H", "H"),],
)
def test_perturb_delete(word, expected_result):
    random.seed(42)
    assert perturb.delete(word) == expected_result


def test_perturb_delete_with_character_size_less_than_three():
    with pytest.raises(AssertionError):
        perturb.delete("To", ignore=False)


def test_perturb_delete_with_whitespace():
    with pytest.raises(AssertionError):
        perturb.delete("is wrong", ignore=False)


@pytest.mark.parametrize(
    "word, expected_result", [("Bob", "B ob"), ("Hey there", "Hey there"), ("H", "H"),],
)
def test_perturb_insert_space(word, expected_result):
    random.seed(42)
    assert perturb.insert_space(word) == expected_result


def test_perturb_insert_space_with_whitespace():
    with pytest.raises(AssertionError):
        perturb.insert_space("is wrong", ignore=False)


def test_perturb_insert_space_with_character_size_less_than_two():
    with pytest.raises(AssertionError):
        perturb.insert_space("H", ignore=False)


@pytest.mark.parametrize(
    "word, expected_result",
    [("EXTRA", "ETXRA"), ("Hey there", "Hey there"), ("H", "H"),],
)
def test_perturb_swap(word, expected_result):
    random.seed(42)
    assert perturb.swap(word) == expected_result


def test_perturb_swap_with_character_size_less_than_four():
    with pytest.raises(AssertionError):
        perturb.swap("Ton")


def test_perturb_swap_with_whitespace():
    with pytest.raises(AssertionError):
        perturb.swap("is wrong")

_author_ = "Rohit Patil"

import random

import pytest

from decepticonlp.transforms import perturbations

WHITE_SPACE_EXAMPLE = "is wrong"


@pytest.mark.parametrize(
    "word, expected_result", [("Bob", "Bb"), ("Hey there", "Hey there"), ("H", "H")]
)
def test_perturb_delete(word, expected_result):
    random.seed(42)
    delete_perturbations = perturbations.DeleteCharacterPerturbations()
    assert delete_perturbations.apply(word) == expected_result


def test_perturb_delete_with_character_size_less_than_three():
    delete_perturbations = perturbations.DeleteCharacterPerturbations()
    with pytest.raises(AssertionError):
        delete_perturbations.apply("To", ignore=False)


def test_perturb_delete_with_whitespace():
    delete_perturbations = perturbations.DeleteCharacterPerturbations()
    with pytest.raises(AssertionError):
        delete_perturbations.apply(WHITE_SPACE_EXAMPLE, ignore=False)


@pytest.mark.parametrize(
    "word, expected_result", [("Bob", "B ob"), ("Hey there", "Hey there"), ("H", "H")]
)
def test_perturb_insert_space(word, expected_result):
    random.seed(42)
    space_perturb = perturbations.InsertSpaceCharacterPerturbations()
    assert space_perturb.apply(word) == expected_result


def test_perturb_insert_space_with_whitespace():
    space_perturb = perturbations.InsertSpaceCharacterPerturbations()
    with pytest.raises(AssertionError):
        space_perturb.apply(WHITE_SPACE_EXAMPLE, ignore=False)


def test_perturb_insert_space_with_character_size_less_than_two():
    space_perturb = perturbations.InsertSpaceCharacterPerturbations()
    with pytest.raises(AssertionError):
        space_perturb.apply("H", ignore=False)


@pytest.mark.parametrize(
    "word, expected_result",
    [("hello", "hellzo"), ("Hey there", "Hey there"), ("H", "H")],
)
def test_perturb_insert_character(word, expected_result):
    random.seed(30)
    char_perturb = perturbations.InsertSpaceCharacterPerturbations()
    assert char_perturb.apply(word, char_perturb=True) == expected_result


@pytest.mark.parametrize("word, expected_result", [("THAT", "TAHT")])
def test_perturb_shuffle_swap_two(word, expected_result):
    random.seed(0)
    shuffle_perturbations = perturbations.ShuffleCharacterPerturbations()
    assert shuffle_perturbations.apply(word, mid=False) == expected_result


@pytest.mark.parametrize(
    "word, expected_result", [("Adversarial", "Aiavrsedarl"), ("dog", "dog")]
)
def test_perturb_shuffle_middle(word, expected_result):
    random.seed(0)
    shuffle_perturbations = perturbations.ShuffleCharacterPerturbations()
    assert shuffle_perturbations.apply(word) == expected_result


def test_perturb_shuffle_with_character_size_less_than_four():
    shuffle_perturbations = perturbations.ShuffleCharacterPerturbations()
    with pytest.raises(AssertionError):
        shuffle_perturbations.apply("Ton", ignore=False)


def test_perturb_shuffle_with_whitespace():
    shuffle_perturbations = perturbations.ShuffleCharacterPerturbations()
    with pytest.raises(AssertionError):
        shuffle_perturbations.apply(WHITE_SPACE_EXAMPLE, ignore=False)


@pytest.mark.parametrize(
    "word, expected_result", [("Noise", "Noixe"), ("Hi there", "Hi there")]
)
def test_perturb_typo(word, expected_result):
    random.seed(0)
    type_perturbations = perturbations.TypoCharacterPerturbations()
    assert type_perturbations.apply(word) == expected_result


def test_perturb_typo_with_whitespace():
    type_perturbations = perturbations.TypoCharacterPerturbations()
    with pytest.raises(AssertionError):
        type_perturbations.apply(WHITE_SPACE_EXAMPLE, probability=0.1, ignore=False)

_author_ = "Somesh Singh"

import random
import pytest
from decepticonlp.extractor import basic


@pytest.mark.parametrize(
    "words, expected_result",
    [(["Hey", "There", "Somesh"], [1]), (["Hey", "there"], [1])],
)
def test_perturb_delete(words, expected_result):
    random.seed(0)
    random_extractor = basic.RandomImportantWordExtractor()
    assert random_extractor.extract(words) == expected_result


@pytest.mark.parametrize(
    "words, expected_result", [(["Raju", "Is", "NLP", "GAWD"], [3, 0])]
)
def test_perturb_delete(words, expected_result):
    random.seed(0)
    random_extractor = basic.RandomImportantWordExtractor()
    assert random_extractor.extract(words, top_k=2) == expected_result


"""
def test_perturb_delete_with_character_size_less_than_three():
    delete_perturbations = perturbations.DeleteCharacterPerturbations()
    with pytest.raises(AssertionError):
        delete_perturbations.apply("To", ignore=False)
"""

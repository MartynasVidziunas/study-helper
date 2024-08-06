import pytest
from questions import FreeFormQuestion

@pytest.fixture
def free_form_question():
    return FreeFormQuestion(
        prompt="What is the capital of France?",
        answer="Paris"
    )

def test_free_form_question_initialization(free_form_question):
    assert free_form_question.prompt == "What is the capital of France?"
    assert free_form_question.answer == "Paris"
    assert free_form_question.active is True
    assert free_form_question.asked == 0
    assert free_form_question.correctly_answered == 0

def test_free_form_question_display(free_form_question, capfd):
    free_form_question.display()
    captured = capfd.readouterr()
    expected_output = (
        "Free-form Question: What is the capital of France?\n"
        "Correct answer: Paris\n"
    )
    assert captured.out == expected_output

def test_free_form_question_check_answer_correct(free_form_question):
    assert free_form_question.check_answer("Paris") is True
    assert free_form_question.asked == 1
    assert free_form_question.correctly_answered == 1

def test_free_form_question_check_answer_incorrect(free_form_question):
    assert free_form_question.check_answer("London") is False
    assert free_form_question.asked == 1
    assert free_form_question.correctly_answered == 0

def test_free_form_question_check_answer_case_insensitive(free_form_question):
    assert free_form_question.check_answer("paris") is True
    assert free_form_question.asked == 1
    assert free_form_question.correctly_answered == 1

def test_free_form_question_check_answer_whitespace(free_form_question):
    assert free_form_question.check_answer("  Paris  ") is True
    assert free_form_question.asked == 1
    assert free_form_question.correctly_answered == 1

def test_free_form_question_to_dict(free_form_question):
    expected_dict = {
        'type': 'FreeFormQuestion',
        'prompt': "What is the capital of France?",
        'active': True,
        'asked': 0,
        'correctly_answered': 0,
        'answer': "Paris"
    }
    assert free_form_question.to_dict() == expected_dict

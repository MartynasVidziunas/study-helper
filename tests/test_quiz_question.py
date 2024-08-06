import pytest
from questions import QuizQuestion

@pytest.fixture
def quiz_question():
    return QuizQuestion(
        prompt="What is the capital of France?",
        choices=["Paris", "London", "Berlin", "Rome"],
        answer="Paris"
    )

def test_quiz_question_initialization(quiz_question):
    assert quiz_question.prompt == "What is the capital of France?"
    assert quiz_question.choices == ["Paris", "London", "Berlin", "Rome"]
    assert quiz_question.answer == "Paris"
    assert quiz_question.active is True
    assert quiz_question.asked == 0
    assert quiz_question.correctly_answered == 0

def test_quiz_question_display(quiz_question, capfd):
    quiz_question.display()
    captured = capfd.readouterr()
    expected_output = (
        "Quiz Question: What is the capital of France?\n"
        "1. Paris\n"
        "2. London\n"
        "3. Berlin\n"
        "4. Rome\n"
        "Correct answer: Paris\n"
    )
    assert captured.out == expected_output

def test_quiz_question_check_answer_correct(quiz_question):
    assert quiz_question.check_answer("Paris") is True
    assert quiz_question.asked == 1
    assert quiz_question.correctly_answered == 1

def test_quiz_question_check_answer_incorrect(quiz_question):
    assert quiz_question.check_answer("London") is False
    assert quiz_question.asked == 1
    assert quiz_question.correctly_answered == 0

def test_quiz_question_to_dict(quiz_question):
    expected_dict = {
        'type': 'QuizQuestion',
        'prompt': "What is the capital of France?",
        'active': True,
        'asked': 0,
        'correctly_answered': 0,
        'choices': ["Paris", "London", "Berlin", "Rome"],
        'answer': "Paris"
    }
    assert quiz_question.to_dict() == expected_dict

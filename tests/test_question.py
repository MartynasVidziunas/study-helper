import pytest
from questions import Question

@pytest.fixture
def question():
    return Question(prompt="What is the capital of France?")

def test_initialization(question):
    assert question.prompt == "What is the capital of France?"
    assert question.active is True
    assert question.asked == 0
    assert question.correctly_answered == 0

def test_add_asked(question):
    question.add_asked()
    assert question.asked == 1

def test_add_correctly_answered(question):
    question.add_correctly_answered()
    assert question.correctly_answered == 1

def test_set_active(question):
    question.set_active(False)
    assert question.active is False
    question.set_active(True)
    assert question.active is True

def test_to_dict(question):
    expected_dict = {
        'type': 'Question',
        'prompt': "What is the capital of France?",
        'active': True,
        'asked': 0,
        'correctly_answered': 0
    }
    assert question.to_dict() == expected_dict

def test_from_dict():
    data = {
        'type': 'Question',
        'prompt': "What is the capital of France?",
        'active': True,
        'asked': 0,
        'correctly_answered': 0
    }
    with pytest.raises(ValueError):
        Question.from_dict(data)

def test_display_not_implemented(question):
    with pytest.raises(NotImplementedError):
        question.display()

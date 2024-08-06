from .question import Question

class QuizQuestion(Question):

    def __init__(self, prompt, choices, answer, asked=0, correctly_answered=0, active=True):
        super().__init__(prompt, asked, correctly_answered)
        self.choices = choices
        self.answer = answer
        self.active = active

    def display(self):
        print(f"Quiz Question: {self.prompt}")
        for i, choice in enumerate(self.choices):
            print(f"{i + 1}. {choice}")
        print(f"Correct answer: {self.answer}")

    def check_answer(self, user_answer):
        self.add_asked()
        if user_answer == self.answer:
            self.add_correctly_answered()
            return True
        return False
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'choices': self.choices,
            'answer': self.answer
        })
        return data
from .question import Question

class FreeFormQuestion(Question):
    
    def __init__(self, prompt, answer, asked=0, correctly_answered=0, active=True):
        super().__init__(prompt, asked, correctly_answered)
        self.answer = answer
        self.active = active

    def display(self):
        print(f"Free-form Question: {self.prompt}")
        print(f"Correct answer: {self.answer}")

    def check_answer(self, user_answer):
        self.add_asked()
        if user_answer.strip().lower() == self.answer.strip().lower():
            self.add_correctly_answered()
            return True
        return False
    
    def to_dict(self):
        data = super().to_dict()
        data.update({
            'answer': self.answer
        })
        return data
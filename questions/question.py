class Question:

    def __init__(self, prompt, asked=0, correctly_answered=0):
        self.prompt = prompt
        self.active = True
        self.asked = asked
        self.correctly_answered = correctly_answered

    def display(self):
        raise NotImplementedError("Subclasses should use this method")
    
    def to_dict(self):
        return {
            'type': self.__class__.__name__,
            'prompt': self.prompt,
            'active': self.active,
            'asked': self.asked,
            'correctly_answered': self.correctly_answered
        }
    
    def add_asked(self):
        self.asked += 1

    def add_correctly_answered(self):
        self.correctly_answered += 1

    def set_active(self, active: bool):
        self.active = active

    
    @staticmethod
    def from_dict(data):
        question_type = data['type']
        if question_type == 'QuizQuestion':
            from .quiz_question import QuizQuestion
            return QuizQuestion(data['prompt'], data['choices'], data['answer'], data['asked'], 
                                data['correctly_answered'], data['active'])
        elif question_type == 'FreeFormQuestion':
            from .free_form_question import FreeFormQuestion
            return FreeFormQuestion(data['prompt'], data['answer'], data['asked'], data['correctly_answered'], data['active'])
        else:
            raise ValueError(f"Unknown question type: {question_type}")
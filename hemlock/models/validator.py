from hemlock import db

class Validator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    condition = db.Column(db.PickleType)
    message = db.Column(db.Text)
    
    def __init__(self, question, condition, message=None):
        self.question = question
        self.set_condition(condition)
        self.set_message(message)
        db.session.add(self)
        db.session.commit()
        
    def set_condition(self, condition):
        self.condition = condition
        
    def set_message(self, message=None):
        self.message = message
        
    def validate(self):
        return self.condition(self.question)
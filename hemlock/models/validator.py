from hemlock import db

class Validator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    condition = db.Column(db.PickleType)
    args = db.Column(db.PickleType)
    
    def __init__(self, question, condition, args=None):
        self.question = question
        self.set_condition(condition, args)
        db.session.add(self)
        db.session.commit()
        
    def set_condition(self, condition, args=None):
        self.condition = condition
        self.args = args
        
    # returns error message if response was invalid
    # returns None if response was valid
    def get_error(self):
        if self.args is None:
            return self.condition(self.question)
        return self.condition(self.question, self.args)
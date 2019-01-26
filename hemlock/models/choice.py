


from hemlock import db

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    text = db.Column(db.Text)
    value = db.Column(db.PickleType)
    
    def __init__(self, question=None, text='', value=None):
        self.question = question
        self.set_text(text)
        self.set_value(value)
        db.session.add(self)
        db.session.commit()
        
    def set_text(self, text=''):
        self.text = text
        
    def set_value(self, value=None):
        if value is None:
            self.value = self.text
        else:
            self.value = value
    
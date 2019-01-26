


from hemlock import db

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    text = db.Column(db.Text)
    value = db.Column(db.PickleType)
    order = db.Column(db.Integer)
    
    def __init__(self, question=None, text='', value=None, order=None):
        self.question = question
        self.set_text(text)
        self.set_value(value)
        self.set_order(order)
        db.session.add(self)
        db.session.commit()
        
    def set_text(self, text=''):
        self.text = text
        
    def set_value(self, value=None):
        if value is None:
            self.value = self.text
        else:
            self.value = value
            
    def set_order(self, order=None):
        if order is None:
            order = len(self.question.choices.all()) - 1
        self.order = order
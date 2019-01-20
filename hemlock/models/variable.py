from hemlock import db

class Variable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    name = db.Column(db.Text)
    data = db.Column(db.PickleType)
    
    def __init__(self, part, name):
        self.part = part
        self.name = name
        self.data = []
        db.session.add(self)
        db.session.commit()
        
    def add_data(self, data):
        self.data.append(str(data))
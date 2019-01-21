from hemlock import db

class Variable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    name = db.Column(db.String)
    data = db.Column(db.PickleType, default=[])
    
    def __init__(self, part, name):
        self.part = part
        self.name = name
        db.session.add(self)
        db.session.commit()
        
    def add_data(self, data):
        self.data = self.data + [data]
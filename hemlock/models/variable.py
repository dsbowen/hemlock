from hemlock import db

class Variable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    name = db.Column(db.String)
    data = db.Column(db.PickleType, default=[])
    num_rows = db.Column(db.Integer, default=0)
    all_rows = db.Column(db.Boolean, default=False)
    
    def __init__(self, part, name, all_rows):
        self.part = part
        self.name = name
        self.all_rows = all_rows
        db.session.add(self)
        db.session.commit()
        
    def add_data(self, data):
        self.data = self.data + [data]
        self.num_rows += 1
        if self.num_rows > self.part.num_rows:
            self.part.num_rows = self.num_rows
        
    def pad(self, length):
        if length <= self.num_rows:
            return
        if self.all_rows and self.data:
            self.data = [self.data[0]]*length
        else:
            self.data = self.data + ['']*(length-self.num_rows)
        self.num_rows = length
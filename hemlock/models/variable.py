###############################################################################
# Variable model
# by Dillon Bowen
# last modified 01/21/2019
###############################################################################

from hemlock import db

# Data:
# ID of participant to whom the variable belongs
# Variable name
# List of data
# Number of rows
# All_rows indicator
#   i.e. whether the same data will appear in all rows of this variable
class Variable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    name = db.Column(db.String)
    data = db.Column(db.PickleType, default=[])
    num_rows = db.Column(db.Integer, default=0)
    all_rows = db.Column(db.Boolean, default=False)
    
    # Add variable to database and commit upon initialization
    def __init__(self, part, name, all_rows):
        self.part = part
        self.name = name
        self.all_rows = all_rows
        db.session.add(self)
        db.session.commit()
        
    # Add data to the variable
    # update number of rows for variable and participant
    def add_data(self, data):
        self.data = self.data + [data]
        self.num_rows += 1
        if self.num_rows > self.part.num_rows:
            self.part.num_rows = self.num_rows
        
    # Pad
    # fills in data if the number of rows is short of length
    # padding is either the same data (for an all_rows variable) or empyty
    def pad(self, length):
        if length <= self.num_rows:
            return
        if self.all_rows and self.data:
            self.data = [self.data[0]]*length
        else:
            self.data = self.data + ['']*(length-self.num_rows)
        self.num_rows = length
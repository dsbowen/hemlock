###############################################################################
# Variable model
# by Dillon Bowen
# last modified 01/21/2019
###############################################################################

from hemlock import db

'''
Data:
part_id: ID of participant to whom the variable belongs
name: variable name
data: list of variable data
num_rows: number of rows of data (len of data list)
all_rows: indicates that the variable has the same data for all dataset rows
'''
class Variable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    name = db.Column(db.String)
    data = db.Column(db.PickleType, default=[])
    num_rows = db.Column(db.Integer, default=0)
    all_rows = db.Column(db.Boolean, default=False)
    
    # Add variable to database and commit upon initialization
    def __init__(self, part, name, all_rows, data=None):
        db.session.add(self)
        db.session.commit()
        self.part = part
        self.name = name
        self.all_rows = all_rows
        self.add_data(data)
        
    # Add data to the variable
    # update number of rows for variable and participant
    def add_data(self, data):
        if data is None:
            return
        self.data = self.data + [data]
        self.num_rows += 1
        if self.num_rows > self.part.num_rows:
            self.part.num_rows = self.num_rows
        
    # Pad
    # fill in data if the number of rows is short of length
    # padding is either the same data (for an all_rows variable) or empty
    def pad(self, length):
        if length <= self.num_rows:
            return
        if self.all_rows and self.data:
            self.data = [self.data[0]]*length
        else:
            self.data = self.data + ['']*(length-self.num_rows)
        self.num_rows = length
        
    def set_num_rows(self, num_rows):
        self.num_rows = num_rows
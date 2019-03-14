###############################################################################
# Visitors table
# tracks visitors to the survey (not only participants)
# by Dillon Bowen
# last modified 03/13/2019
###############################################################################

from hemlock.factory import db
from copy import deepcopy

class Visitors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ipv4 = db.Column(db.PickleType, default=[])
    
    def __init__(self):
        db.session.add(self)
        db.session.commit()
    
    # Append ipv4 address
    def append(self, ipv4):
        if ipv4 in self.ipv4:
            return
        temp = deepcopy(self.ipv4)
        temp.append(ipv4)
        self.ipv4 = deepcopy(temp)
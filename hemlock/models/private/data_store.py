###############################################################################
# Data Store model
# by Dillon Bowen
# last modified 03/22/2019
###############################################################################

from hemlock.factory import db
from copy import deepcopy
import pandas as pd

class DataStore(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    data = db.Column(db.PickleType, default={})
    
    def __init__(self):
        db.session.add(self)
        db.session.commit()
        
    # Add data from given participant
    # set the variable order
    # collect participant data in padded dictionary
        # {'var_name':{'all_rows': Bool, 'data': list}}
    # union with global dataset
    def add(self, part):
        self.set_vorder(part)
        
        part_data = deepcopy(part._metadata)
        questions = sorted(part._questions.all(), key=lambda q: q.id)
        [self.process_question(part_data, q) 
            for q in questions if q._var is not None]
        self.pad_data(part_data)
            
        union = pd.concat(
            [pd.DataFrame.from_dict(self.data),
             pd.DataFrame.from_dict(part_data)])
        self.data = deepcopy(union.to_dict())
        
    # Set the question variable order (vorder)
    def set_vorder(self, part):
        vars = list(set([q._var for q in part._questions]))
        vars = [v for v in vars if v is not None]
        for v in vars:
            qlist = part._questions.filter_by(_var=v).all()
            [qlist[i]._set_vorder(i) for i in range(len(qlist))]
            
    # Process question data
    # pad variables in participant data dictionary to equal length
    # write question data to participant data
    def process_question(self, part_data, q):
        qdata = q._output_data()
        vars = qdata.keys()
        for v in vars:
            if v not in part_data:
                part_data[v] = {'all_rows': q._all_rows, 'data': []}
        self.pad_data(part_data, vars)
        [part_data[v]['data'].extend(qdata[v]) for v in vars]
        
    # Pad participant dataset
    # arguments:
        # vars: ['var_name'] (keys for part_data)
    def pad_data(self, part_data, vars=None):
        if vars is None:
            vars = part_data.keys()
        length = max([len(part_data[v]['data']) for v in vars])
        [self.pad_var(part_data[v], length) for v in vars]
        
    # Pad a single variable
    # arguments:
        # var: {'all_rows': Bool, 'data': list}
    def pad_var(self, var, length):
        if var['all_rows'] and var['data']:
            var['data'] = var['data'][-1]*length
            return
        var['data'] += ['']*(length-len(var['data']))
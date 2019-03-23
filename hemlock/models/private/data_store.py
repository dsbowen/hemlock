###############################################################################
# Data Store model
# by Dillon Bowen
# last modified 03/23/2019
###############################################################################

from hemlock.factory import db
from copy import deepcopy

class DataStore(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    data = db.Column(db.PickleType, default={})
    num_rows = db.Column(db.Integer, default=0)
    part_ids = db.Column(db.PickleType, default=[])
    
    def __init__(self):
        db.session.add(self)
        db.session.commit()
        
    # Add data from given participant
    # remove from dataset if participant was previously stored
    # initialize participant data dictionary using metadata
        # format: {'var_name':{'all_rows': Bool, 'data': list}}
    # set the variable order
    # add question data to participant data dictionary
    # union with global dataset
    def store(self, part):
        self.remove(part)
    
        part_data = {var:{'all_rows': True, 'data': [val]} 
                        for var, val in part._metadata.items()}
    
        self.set_vorder(part)
                        
        questions = sorted(part._questions.all(), key=lambda q: q.id)
        [self.process_question(part_data, q) 
            for q in questions if q._var is not None]
        new_rows = self.pad_data(part_data)
            
        self.union_part_data(part.id, part_data, new_rows)
        self.part_ids = self.part_ids + [part.id]
             
    # Remove a participant from the dataset
    # id: id of participant to be removed
    def remove(self, part):
        if part.id not in self.part_ids:
            return
            
        start = self.data['id'].index(part.id)
        end = self.data['id'][::-1].index(part.id)
        temp = deepcopy(self.data)
        for v in temp.keys():
            temp[v] = temp[v][:start] + temp[v][end:]
            
        self.data = deepcopy(temp)
        self.part_ids = [id for id in self.part_ids if id!=part.id]
        
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
        [part_data[v]['data'].extend([qdata[v]]) for v in vars]
        
    # Pad participant dataset
    # arguments:
        # vars: ['var_name'] (keys for part_data)
    def pad_data(self, part_data, vars=None):
        if vars is None:
            vars = part_data.keys()
        length = max([len(part_data[v]['data']) for v in vars])
        [self.pad_var(part_data[v], length) for v in vars]
        return length
        
    # Pad a single variable
    # arguments:
        # var: {'all_rows': Bool, 'data': list}
    def pad_var(self, var, length):
        if var['all_rows'] and var['data']:
            var['data'] = [var['data'][-1]] * length
            return
        var['data'] += ['']*(length-len(var['data']))
        
    # Union the survey dataset with the participant's dataset
    # arguments:
        # new_rows: number of new rows being added to dataset by participant
    # pad data for variables unique to participant data
    # add participant data to variables common to data and part_data
    # pad data for variables unique to (global) data
    # update data, participant index, number of rows
    def union_part_data(self, id, part_data, new_rows):
        temp = deepcopy(self.data)
        
        part_data_vars = [v for v in part_data.keys() if v not in temp]
        for v in part_data_vars:
            temp[v] = ['']*self.num_rows
            
        intersect_vars = [v for v in part_data.keys() if v in temp]
        [temp[v].extend(part_data[v]['data']) for v in intersect_vars]
        
        data_vars = [v for v in temp.keys() if v not in part_data]
        [temp[v].extend(['']*new_rows) for v in data_vars]
        
        self.data = deepcopy(temp)
        self.num_rows += new_rows
        
    # Print the data
    # for debuggin purposes only
    def print_data(self):
        for v in self.data.keys():
            print(v, self.data[v])
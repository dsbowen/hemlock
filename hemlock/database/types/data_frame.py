"""DataFrame mutable object and column type"""

from copy import copy
from datetime import timedelta
from flask import current_app
from io import StringIO
from sqlalchemy import PickleType
from sqlalchemy_mutable import MutableList, MutableDict
import csv
import os


class Variable(MutableList):
    def __init__(self, all_rows=False):
        """
        all_rows indicates that all rows belonging to this variable should be the same.
        """
        self._python_type = None
        self.all_rows = all_rows
        super().__init__()
        
    def add(self, entry):
        """Add an entry (or list of entries) to the variable"""
        if isinstance(entry, list):
            self += entry
        else:
            self.append(entry)
    
    def pad(self, rows):
        """Pad the entries
        
        Add padding so that the Variable length is equal to rows.
        """
        val = self[-1] if self and self.all_rows else None
        self += [val]*(rows-len(self))


class DataFrame(MutableDict):
    @classmethod
    def coerce(cls, key, value):
        if isinstance(value, cls):
            return value
        if isinstance(value, dict):
            return cls(value)
        return super().coerce(key, value)

    def __init__(self, value={}):
        self._python_type = None
        super().__init__(value)

    def rows(self, variables=None):
        """Number of rows
        
        Return the maximum number of rows associated with a given subset of
        variables. If variables is not given, set variables to all variables
        in the DataFrame.
        """
        variables = variables or self.keys()
        lengths = [len(self[var]) for var in variables if var in self]
        return max(lengths) if lengths else 0
        
    def append(self, data, all_rows=False):
        self.pad()
        self.add(data, all_rows, rows=self.rows())
        self.pad()
    
    def add(self, data, all_rows=False, rows=None):
        """Add data dictionary to the DataFrame
        
        all_rows indicates that the Variables associated with these data
        should have the same value for all rows of the DataFrame.
        """
        self._changed()
        rows = rows or self.rows(data.keys())
        [self.prep_variable(var, all_rows, rows) for var in data.keys()]
        [self[var].add(entry) for var, entry in data.items()]
        
    def prep_variable(self, var, all_rows=False, rows=None):
        """Prepare a variable for adding an entry
        
        Add the variable if it is not yet in the DataFrame and pad.
        """
        rows = self.rows() if rows is None else rows
        if var not in self:
            self[var] = Variable(all_rows)
        self[var].pad(rows)
    
    def remove(self, start, end):
        """Remove data between start and end indices"""
        self._changed()
        for var in self.keys():
            modified_data = self[var][:start] + self[var][end:]
            self[var] = Variable(self[var].all_rows)
            self[var].add(modified_data)
    
    def pad(self):
        """Pad DataFrame so all Variables have the same number of rows"""
        self._changed()
        rows = self.rows()
        [self[var].pad(rows) for var in self.keys()]

    def get_download_file(self):
        """Get file download tuple
        
        File download is (filename, file string) tuple.
        """
        csv_str = StringIO()
        writer = csv.writer(csv_str)
        writer.writerow(self.keys())
        writer.writerows(zip(*self.values()))
        return (self.filename, csv_str)


class DataFrameType(PickleType):
    pass


DataFrame.associate_with(DataFrameType)
###############################################################################
# query function
# by Dillon Bowen
# last modified 01/21/2019
###############################################################################

from hemlock.models.question import Question

# Return objects from query by id
# if id is an integer, return a single object
# if id is a list, return a list of objects
# if id is a dict, return a dict of objects with corresponding keys
def query(ids, model_type=Question):
    if type(ids) == int:
        return model_type.query.get(ids)
    if type(ids) == list:
        return model_type.query.filter(model_type.id.in_(ids)).all()
    if type(ids) == dict:
        return {key:model_type.query.get(value) for (key,value) in ids.items()}
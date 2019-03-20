###############################################################################
# query function
# by Dillon Bowen
# last modified 03/13/2019
###############################################################################

from hemlock.models.question import Question

# Return objects from query by id
# to_get may be an id (integer), list, or dict
# nested lists and dictionaries are allowed
def query(to_get, table=Question):
    if type(to_get) == int:
        return table.query.get(to_get)
    if type(to_get) == list:
        return [query(x, table) for x in to_get]
    if type(to_get) == dict:
        return {key:query(x, table) for (key,x) in to_get.items()}
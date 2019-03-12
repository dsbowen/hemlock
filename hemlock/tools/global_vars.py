###############################################################################
# Global dictionary handling
# by Dillon Bowen
# last modified 03/12/2019
###############################################################################

from flask_login import current_user

# Modify the global dictionary for the current participant
def modg(modification):
    current_user.modg(modification)
    
# Return a value of the global dictionary for a given set of keys
# return None for keys not in dictionary
def g(keys):
    return current_user.g(keys)
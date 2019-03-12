###############################################################################
# Global dictionary handling
# by Dillon Bowen
# last modified 02/19/2019
###############################################################################

from flask_login import current_user

# Modify the global dictionary for the current participant
def modg(modification):
    current_user.modg(modification)
    
# Return a value of the global dictionary for a given key
# return None if key is not in dictionary 
def g(key):
    return current_user.get_g(key)
##############################################################################
# Model shell class
# by Dillon Bowen
# last modified 09/03/2019
##############################################################################

class ModelShell():
    def __init__(self, model):
        self.id = model.id
        self.model_class = model.__class__
        
    def unshell(self):
        return self.model_class.query.get(self.id)
        
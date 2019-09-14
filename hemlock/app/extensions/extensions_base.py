##############################################################################
# Base for hemlock extensions
# by Dillon Bowen
# last modified 08/17/2019
##############################################################################

class ExtensionsBase():
    def _register_app(self, app, ext_name):
        self.app = app
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions[ext_name] = self
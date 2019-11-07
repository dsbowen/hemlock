"""Base for Hemlock extensions"""

class ExtensionsBase():
    def _register_app(self, app, ext_name):
        self.app = app
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions[ext_name] = self
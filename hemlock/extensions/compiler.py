##############################################################################
# Html compiler class
# by Dillon Bowen
# last modified 08/14/2019
##############################################################################

from hemlock.extensions.extensions_base import ExtensionsBase
from hemlock.extensions.compile_texts import *

class Compiler(ExtensionsBase):
    def __init__(self):
        self.compiler_functions = {}

    # Register question type to compiler function mapping
    def register(self, qtype, overwrite=True):
        def original_function(f):
            if qtype not in self.compiler_functions or overwrite:
                self.compiler_functions[qtype] = f
            return f
        return original_function
    
    # Initialize with app
    def init_app(self, app):
        import hemlock.extensions.compile_functions
        self._register_app(app, 'compiler')
    
    # Compile html for a page
    def compile_page(self, p):
        page_id = PAGE_ID.format(pid=p.id)
        questions = p.get_questions()
        qhtml = ''.join([self.compile_question(q) for q in questions])
        submit_html = self.submit(p)
        return ''.join([page_id, qhtml, submit_html])

    # Compile html for a question
    def compile_question(self, q):
        return self.compiler_functions[q.get_qtype()](q)

    # Submit button
    def submit(self, p):
        html = BREAK
        if p._back:
            html += BACK_BUTTON
        if not p._terminal:
            html += FORWARD_BUTTON
        return html + PAGE_BREAK 
    
    
        
    
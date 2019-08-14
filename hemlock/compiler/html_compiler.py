##############################################################################
# Html compiler class
# by Dillon Bowen
# last modified 08/14/2019
##############################################################################

from hemlock.compiler.html_texts import *

class Compiler():
    def __init__(self):
        self.compiler_functions = {}

    # Register question type to compiler function mapping
    def register(self, qtype):
        def original_function(f):
            self.compiler_functions[qtype] = f
            return f
        return original_function
    
    # Initialize with app
    def init_app(self, app):
        import hemlock.compiler.compile_functions
    
    # Compile html for a page
    def compile_page(self, p):
        page_id = PAGE_ID.format(pid=p.id)
        questions = p.get_questions()
        qhtml = ''.join([self.compile_question(q) for q in questions])
        submit_html = self.submit(p)
        return ''.join([page_id, qhtml, submit_html])

    # Compile html for a question
    def compile_question(self, q):
        print(q.get_qtype())
        return self.compiler_functions[q.get_qtype()](q)

    # Submit button
    def submit(self, p):
        html = BREAK
        if p._back:
            html += BACK_BUTTON
        if not p._terminal:
            html += FORWARD_BUTTON
        return html + PAGE_BREAK 
    
    
        
    
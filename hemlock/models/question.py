from hemlock import db

def render_text(q):
    return q.text
    
def render_free(q):
    html = render_text(q) + '\n<br>\n'
    html += "<input name='" + str(q.id) + "' type='text' value='" + q.default + "'>\n"
    return html

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qtype = db.Column(db.String(16), default='text')
    text = db.Column(db.Text, default='')
    default = db.Column(db.Text, default='')
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    data = db.Column(db.Text)
    
    def set_qtype(self, qtype):
        self.qtype = qtype
    
    def set_text(self, text):
        self.text = text
        
    def set_default(self, default):
        self.default = default
        
    def set_data(self, data):
        self.data = data
        
    def assign_page(self, page):
        self.page = page
        
    def render(self):
        rendered_html = '<p>\n'
        if self.qtype == 'text':
            rendered_html += render_text(self)
        if self.qtype == 'free':
            rendered_html += render_free(self)
        return rendered_html + '\n</p>\n'
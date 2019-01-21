from hemlock import db
# from hemlock.models.page import Page

def render_text(q):
    return q.text
    
def render_free(q):
    html = render_text(q) + '\n<br>\n'
    html += "<input name='" + str(q.id) + "' type='text' value='" + q.default + "'>\n"
    return html

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    qtype = db.Column(db.String(16))
    var = db.Column(db.Text)
    text = db.Column(db.Text)
    default = db.Column(db.Text)
    data = db.Column(db.Text)
    order = db.Column(db.Integer)
    all_rows = db.Column(db.Boolean)
    
    def __init__(self, page=None, order=None, var=None, qtype='text', text='', default='',
        data=None, all_rows=False):
        
        self.set_qtype(qtype)
        self.assign_page(page, order)
        self.set_var(var)
        self.set_text(text)
        self.set_default(default)
        self.set_data(data)
        self.set_all_rows(all_rows)
        db.session.add(self)
        db.session.commit()
    
    # remove from old page
    # assign to new page
    # assign new order
    def assign_page(self, page, order=None):
        if self.page:
            self.page.remove_question(self)
        self.page = page
        self.set_order(order)
        
    def set_order(self, order=None):
        if order is None and self.page:
            order = len(self.page.questions.all()) - 1
        self.order = order
        
    def set_var(self, var):
        self.var = var
        
    def set_qtype(self, qtype):
        self.qtype = qtype
    
    def set_text(self, text):
        self.text = text
        
    def set_default(self, default):
        self.default = default
        
    def set_data(self, data):
        self.data = data
        
    def set_all_rows(self, all_rows):
        self.all_rows = all_rows
        
    def render(self, part):
        self.part = part
        db.session.commit()
        
        rendered_html = '<p>\n'
        if self.qtype == 'text':
            rendered_html += render_text(self)
        if self.qtype == 'free':
            rendered_html += render_free(self)
        return rendered_html + '\n</p>\n'
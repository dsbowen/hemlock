
    p = Page(branch=b)
    greet = Question(page=p, render=greeting, render_args=name.id)
    ice_cream = Question(page=p, var='ice_cream', qtype='single choice')
    ice_cream.set_text("What's your favorite flavor ice cream?")
    c = Choice(question=ice_cream, text='chocolate')
    c = Choice(question=ice_cream, text='vanilla')
    c = Choice(question=ice_cream, text='strawberry')
    v = Validator(question=ice_cream, condition=not_empty, args='Please answer the question.')
    v = Validator(question=ice_cream, condition=not_strawberry)
    
    p = Page(branch=b)
    q = Question(page=p, var='verified', qtype='single choice', render=verify_ice_cream, render_args=ice_cream.id)
    c = Choice(question=q, text='yes', value=1)
    c = Choice(question=q, text='no', value=0)
    
    p = Page(branch=b)
    attn = Question(page=p, var='attention', qtype='free', text='Please enter 99', post=check_attn)
    
    p = Page(branch=b, terminal=True)
    q = Question(page=p, render=pass_fail, render_args=attn.id)
    
    return b
    
def greeting(q, name_id):
    name = query(name_id).data
    q.set_text('Hello, {0}!'.format(name))
    
def verify_ice_cream(q, ice_cream_id):
    ice_cream = query(ice_cream_id)
    selected = ice_cream.get_selected()[0].text
    nonselected = ice_cream.get_nonselected()
    nonselected = [x.text for x in nonselected]
    q.set_text('''
        You said you prefer {0} over {1} and {2}. Is this correct?
        '''.format(selected, nonselected[0], nonselected[1]))
    
def not_empty(question, message):
    if not bool(question.data):
        return message
        
def not_strawberry(q):
    if q.data=='strawberry':
        return "Strawberry is objectively a terrible ice cream flavor. Try again."
    
def check_attn(q):
    q.set_data(int(q.entry=='99'))

def pass_fail(q, attn_id):
    attn = query(attn_id)
    passed, entry = attn.data, attn.entry
    if passed:
        q.set_text('Congratulations! You entered {0} and passed the attention check!'.format(entry))
    else:
        q.set_text('You entered {0} and FAILED the attention check!'.format(entry))
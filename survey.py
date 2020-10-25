from hemlock import Branch, Page, Label, route

@route('/survey')
def start():
    return Branch(
        Page(
            Label('Hello, world!'),
            terminal=True
        )
    )
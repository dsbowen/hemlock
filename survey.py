from hemlock import Branch, Dashboard, Label, Page, route

@route('/survey')
def start():
    return Branch(
        Page(
            Dashboard(src='/dashapp/', var='n_clicks')
        ),
        Page(
            Label('<p>The end.</p>'),
            terminal=True
        )
    )
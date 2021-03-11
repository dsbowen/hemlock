from hemlock import Branch, Page, Label, route

@route('/survey')
def start():
    return Branch(
        Page(
            Label(
                'Start'
            )
        ),
        Page(
            Label(
                'The end'
            ),
            compile_worker=True,
            terminal=True
        )
    )
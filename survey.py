from hemlock import Branch, Page, Input, Label, Compile as C, route

@route('/survey')
def start():
    name_input = Input("What's your name?")
    return Branch(
        Page(
            name_input
        ),
        Page(
            Label(compile=C.greet(name_input)),
            compile_worker=True,
            terminal=True, back=True
        )
    )

@C.register
def greet(greet_label, name_input):
    greet_label.label = "Hello, {}!".format(name_input.response)
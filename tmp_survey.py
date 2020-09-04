from hemlock import Branch, Page, Input, Compile as C, Validate as V, route

@route('/survey')
def start():
    inpt = Input('<p>Enter a number</p>', input_type='number', step='any', validate=V.exact_decimals(2))
    return Branch(
        Page(
            inpt
        ),
        Page(
            compile=C.print_type(inpt),
            terminal=True
        )
    )

@C.register
def print_type(page, inpt):
    print('inpt response is', inpt.response)
    print('inpt response type', type(inpt.response))
    print('inpt data is', inpt.data)
    print('inpt data type', type(inpt.data))
from hemlock import Branch, Compile as C, Label, Page, route

@route('/survey')
def start():
    return Branch(
        Page(
            Label('<p>Hello, World!</p>')
        ),
        Page(
            Label(
                '<p>Goodbye, Moon!</p>',
                compile=C.complex_function(seconds=5)
            ),
            compile_worker=True,
            terminal=True
        ),
    )

@C.register
def complex_function(label, seconds):
    import time
    for t in range(seconds):
        print('Progress: {}%'.format(round(100.*t/seconds)))
        time.sleep(1)
    print('Progress: 100%')
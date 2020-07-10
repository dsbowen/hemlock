Hemlock aspires to be the most powerful and flexible way to create online studies, with applications in marketing and behavioral science research.

If you're new to python, or the installation and quickstart instructions don't make sense to you, check out the [tutorial](https://dsbowen.github.io/hemlock/tutorial/intro/).

## Installation

```bash
$ pip install hemlock-survey
```

## Quickstart

First, create a file `app.py` in the root directory of your project:

```python
import survey

from hemlock import create_app

app = create_app()

if __name__ == '__main__':
    from hemlock.app import socketio
    socketio.run(app, debug=True)
```

Create another file `survey.py` in the same directory:

```python
from hemlock import Branch, Label, Page, route

@route('/survey')
def start():
    return Branch(Page(Label('<p>Hello, World!</p>'), terminal=True))
```

Run your app:

```bash
$ python3 app.py
```

And navigate to <http://localhost:5000/> in your browser.

## Citation

```
@software{bowen2020hemlock,
  author = {Dillon Bowen},
  title = {Hemlock},
  url = {https://dsbowen.github.io/hemlock/},
  date = {2020-07-10},
}
```

## License

Users must cite this package in any publications which use it.

It is licensed with the [Hemlock Research License](https://github.com/dsbowen/hemlock/blob/master/LICENSE). The license permits free use for academic research, and requires written permission from hemlock's author, Dillon Bowen, for commercial use.
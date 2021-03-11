# Hemlock

Hemlock aspires to be the most powerful and flexible way to create online studies, with applications in marketing and behavioral science research.

## New to programming?

If behavioral science research has taught us anything, it's that even small costs can prevent us from investing time and effort into things which ultimately make us better off. Hemlock is one of those things.

If you're an intermediate-level programmer (e.g., comfortable with R, new to python), I estimate it will take you 3 full days of effort to learn the basics of python and hemlock. I want to convince you that putting in those 3 days of effort will save you hundreds of hours over the course of your career and enable you to shatter boundaries in your field.

First, check out <a href="https://hemlock-tutorial.herokuapp.com" target="_blank">this demo</a>. This is the survey you'll build in the hemlock tutorial. In just over 200 lines of code, we build a survey that collects demographic information, gives participants instructions and tests their comprehension, and pairs participants with one another to play an ultimatum game.

Second, check out this binder <a href="https://mybinder.org/v2/gh/dsbowen/hemlock-demo/HEAD/?urlpath=lab" target="_blank">![Binder](https://mybinder.org/badge_logo.svg)</a>. The binder is a sandbox which shows how easy it is to create beautiful hemlock survey pages. Unfortunately, it can't create a full survey. For that, you'll need to run through the hemlock tutorial.

Third, read [this article](manifesto.md) about my vision for hemlock and how it can advance your research.

Finally, block off a long weekend and go through [the tutorial](tutorial/intro.md). I'm dedicated to making hemlock a spectacular service, so if you run into any difficulty, <a href="https://github.com/dsbowen/hemlock/issues" target="_blank">open a github issue</a> and I will personally help fix your issue.

## Contact

If you're a marketing, political advertising, or other for-profit company, see my [contact page](contact.md#for-profit-and-political-research) for details on hiring me as a consultant and purchasing a commercial license.

If you're an academic or non-profit researcher interested in using hemlock, see my [contact page](contact.md#non-profit-and-academic-research) for contact details and collaboration policy.

## Installation

```
$ pip install hemlock-survey
```

## Quickstart

Create a file `app.py` in the root directory of your project:

```python
import eventlet
eventlet.monkey_patch()

from hemlock import Branch, Page, Label, create_app, route

@route('/survey')
def start():
    return Branch(
        Page(
            Label('Hello, World!'),
            terminal=True
        )
    )

app = create_app()

if __name__ == '__main__':
    from hemlock.app import socketio
    socketio.run(app, debug=True)
```

Run your app:

```bash
$ python3 app.py
```

And navigate to <http://localhost:5000/> in your browser.

## Citation

```
@software{bowen2021hemlock,
  author = {Dillon Bowen},
  title = {Hemlock},
  url = {https://dsbowen.github.io/hemlock/},
  date = {2021-02-13},
}
```

## License

Users must cite this package in any publications which use it.

It is licensed with the [Hemlock Research License](https://github.com/dsbowen/hemlock/blob/master/LICENSE). The license permits free use for academic research, and requires written permission from hemlock's author, Dillon Bowen, for commercial use.
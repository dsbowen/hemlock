# Running hemlock locally

In the previous part of the tutorial, you learned how to initialize a hemlock project and create and preview a hemlock page.

By the end of this part of the tutorial, you'll be able to:

1. Initialize a hemlock application.
2. Run your hemlock application locally.

**Note.** Running an app 'locally' means that you can play with it on your own computer, but it won't be available on the internet. We'll cover deployment later.

## Why run locally?

In the previous part of the tutorial, we created and previewed a page in a jupyter notebook. Hemlock + jupyter notebook is great for trying out ideas and iterating quickly, like working on a blackboard. However, it won't create a fully responsive application (survey). For that, we're going to need to run our app locally.

## Running the application

Create a python file called `survey.py` in the root directory of your project. If you're working with Visual Studio Code, enter the following in your terminal:

```bash
$ code survey.py
```

Enter the following code in `survey.py`:

```python
from hemlock import Branch, Page, Label, route

@route('/survey')
def start():
    return Branch(
        Page(
            Label('<p>Hello, World!</p>'), 
            terminal=True
        )
    )
```

To preview your survey, go back to your terminal window and enter:

```bash
$ hlk serve
```

Then navigate to <http://localhost:5000/> in your browser.

### Modifications if not using hemlock-CLI or the hemlock template

The hemlock template comes with an `app.py` file which creates the application instace. Create `app.py` in your root directory with the following code:

```python
import survey

from hemlock import create_app

app = create_app()

if __name__ == '__main__':
    from hemlock.app import socketio
    socketio.run(app, debug=True)
```

Instead of running with `hlk serve`, use:

```bash
$ python3 app.py
```

### Code explanation

After our imports, we use the `@route('/survey')` decorator to register our first 'navigate' function. This essentially tells our application, 'start here'.

Navigate functions direct the 'survey flow'. All navigate functions return `Branch` objects. A `Branch` contains a list of pages which it displays to participants. We set a branch's pages by passing them as arguments the constructor, or by setting a branch's `pages` attribute, meaning that the following are equivalent:

```python
b = Branch(Page(Label('<p>Label 0</p>')), Page(Label('<p>Label 1</p>')))
```

```python
b = Branch()
b.pages = [Page(Label('<p>Label 0</p>')), Page(Label('<p>Label 1</p>'))]
```

We also passed a keyword (named) argument to the page constructor, `terminal=True`. This tells the application 'end here'.

## Summary

In this part of the tutorial, you learned how to tell your application where to start and end, and run your application locally.

In the next part of the tutorial, we're going to add a demographics questionnaire to the beginning of our survey.
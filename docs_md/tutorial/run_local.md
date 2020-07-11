# Running hemlock locally

In the previous part of the tutorial, you learned how to initialize a hemlock project and create and preview a hemlock page.

By the end of this part of the tutorial, you'll be able to initialize a hemlock application and run it locally.

**Note.** Running an app 'locally' means that you can play with it on your own computer, but it won't be available on the internet. We'll cover deployment later.

## Why run locally?

In the previous part of the tutorial, we created and previewed a page in a jupyter notebook. Hemlock + jupyter notebook is great for trying out ideas and iterating quickly, like working on a blackboard. However, it won't create a fully responsive application (survey). For that, we're going to need to run our app locally.

## Running the application

You should have jupyter running in a terminal window from the previous part of the tutorial. Leave it running and open a second terminal window. In general, I recommend having one terminal open for jupyter, and a second for editing python files and running your app.

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

To preview your survey, go to your (second) terminal window and enter:

```bash
$ hlk serve
```

Then navigate to <http://localhost:5000/> in your browser.

#### Modifications if not using hemlock-CLI or the hemlock template

The hemlock template comes with an `app.py` file which creates the application instance. Create `app.py` in your root directory with the following code:

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

## Code explanation

After our imports, we use the `@route('/survey')` decorator to register our first 'navigate' function. This essentially tells our application, 'start here'.

Navigate functions direct the 'survey flow'. All navigate functions return `Branch` objects. A branch contains a list of pages which it displays to participants. We set a branch's pages by passing them as arguments to the constructor, or by setting a branch's `pages` attribute, meaning that the following are equivalent:

```python
b = Branch(Page(Label('<p>Label 0</p>')), Page(Label('<p>Label 1</p>')))
```

```python
b = Branch()
b.pages = [Page(Label('<p>Label 0</p>')), Page(Label('<p>Label 1</p>'))]
```

We also passed a keyword (named) argument to the page constructor, `terminal=True`. This tells the application 'end here'.

## Workflow

In the previous part of the tutorial, we designed a page in jupyter notebook. In this part of the tutorial, we used that design in our survey file. The entire hemlock tutorial follows this general workflow:

1. Iterate quickly on the next part of your survey in jupyter.
2. When you're happy with the design, update your survey files (e.g. `survey.py`).
3. Run the app locally with `hlk serve` (or `python3 app.py`).
4. When you're happy with how the app runs, close the app (click on your terminal and hit Ctrl + C).
5. Repeat.

As the name `blackboard.ipynb` suggests, I treat jupyter like a blackboard. Once I'm happy with a design and it's running in my app, I like to start the next design on a fresh blackboard:

1. Delete every cell in the notebook (except the first, where we push the application context, and the last, where we remove temporary files).
2. Restart the kernel (Kernel >> Restart).
3. Run the first cell to re-push the application context.

You may also want to clear the database after running your app:

```
$ rm data.db
```

## Summary

In this part of the tutorial, you learned how to initialize a hemlock application and run it locally.

In the next part of the tutorial, you'll learn how to use question polymorphs to add a demographics questionnaire to your survey.
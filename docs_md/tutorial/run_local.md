# Running hemlock locally

In the previous part of the tutorial, you learned how to initialize a hemlock project and create and preview a hemlock page.

By the end of this part of the tutorial, you'll be able to initialize a hemlock application and run it locally.

**Note.** Running an app 'locally' means that you can play with it on your own computer, but it won't be available on the internet. We'll cover deployment later.

Click here to see what your <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.0/blackboard.ipynb" target="_blank">`blackboard.ipynb`</a> and <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.0/survey.py" target="_blank">`survey.py`</a> files should look like at the end of this part of the tutorial.

## Why run locally?

In the previous part of the tutorial, we created and previewed a page in a jupyter notebook. Hemlock + jupyter notebook is great for trying out ideas and iterating quickly, like working on a blackboard. However, it won't create a fully responsive application. The application itself derives from `survey.py`. To preview our survey as a fully responsive web application, we need to run our app locally.

## Open a second terminal window

You should have jupyter running in a terminal window from the previous part of the tutorial. Open a second terminal window. In general, I recommend having one terminal open for jupyter, and a second for editing python files and running your app. In the second terminal window, change to your project folder:

```bash
$ cd
$ cd my-first-project
```

<!-- `hlk init` created a virtual environment for your hemlock project. Activate your virtual environment in your second terminal window:

Activate from git bash on Windows:

```bash
$ . hemlock-venv/scripts/activate
```

Activate from Mac, Linux, or WSL:

```bash
$ . hemlock-venv/bin/activate
```

**Note on virtual environments.** In general, you should activate your <a href="https://docs.python.org/3/tutorial/venv.html" target="_blank">virtual environment</a> every time you open a terminal to work on your project. Why use a virtual environment? While your code may work for the latest version of a package today, the next package update may use a different syntax, meaning you'd have to revise all of your code. Virtual environments solve this problem by 'freezing' the current version of your packages in the project to which they belong. -->

## Run your application

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
Prepare to get served.

 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 183-643-336
(2841) wsgi starting up on http://127.0.0.1:5000
```

Then navigate to <http://localhost:5000/> in your browser.

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

#### Troubleshooting

During development, you may encounter a database error from which your app can't recover. Even after you've fixed your code, your database will still be broken. If this happens in your jupyter notebook, simply restart your kernel (Kernel >> Restart) and run your code cells again. If this happens while running your app locally:

1. Exit with Ctrl + C.
2. Remove the database with `rm data.db`.
3. Run your app again with `hlk serve`.

<!-- You may also want to clear the database after running your app:

```
$ rm data.db # del data.db on windows command prompt
``` -->

## Summary

In this part of the tutorial, you learned how to initialize a hemlock application and run it locally.

In the next part of the tutorial, you'll learn how to use question polymorphs to add a demographics questionnaire to your survey.

<!-- #### Modifications if not using hemlock-CLI or the hemlock template

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
``` -->
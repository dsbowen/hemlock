# Your first project

By the end of this part of the tutorial, you'll be able to:

1. Initialize a new hemlock project.
2. Create and preview hemlock survey pages.

## Initialize a new hemlock project

### From the hemlock template (recommended)

I recommend starting hemlock projects from the hemlock template:

```bash
$ hlk init my-first-project
```

This will 'clone' the template into a folder `my-first-project`, set up a virtual environment, and pip install hemlock. Change into the project directory and activate the virtual environment.

```bash
$ cd my-first-project
$ source hemlock-venv/bin/activate
```

It's good practice to use [virtual environments](https://docs.python.org/3/tutorial/venv.html) and activate them whenever you're working on a project.

### Alternatively, from scratch

Create a folder for your project and change into it:

```bash
$ mkdir my-first-project
$ cd my-first-project
```

Create your virtual environment and activate it:

```bash
$ python3 -m venv hemlock-venv
$ source hemlock-venv/bin/activate
```

Install hemlock:

```bash
$ pip3 install hemlock-survey
```

## Preview a page in jupyter notebook

Jupyter notebook is a great tool for iterating quickly on project designs. I recommend using it for most of your work. Open the jupyter dashboard with:

```bash
$ jupyter notebook
```

Jupyter will attempt to open the dashboard automatically in your browser. If this fails, the terminal window will show you links to the dashboard that you can manually copy and paste into your browser.

Open the file named `blackboard.ipynb`. Run the first cell (Shift + Enter on windows) to set up the environment and application context. It's not important right now to understand exactly what it does.

Now, create your first hemlock page. In a new code cell below the first one, enter the following:

```python
from hemlock import Page, Label

p = Page(Label('<p>Hello, World!</p>'))
p.preview() # p.preview('Ubuntu') if running in Ubuntu/WSL
```

This opens a preview of your page in your browser.

**Note.** We'll be previewing pages throughout the tutorial. If you're working in Ubuntu/WSL, always replace `my_page.preview()` with `my_page.preview('Ubuntu')`.

### Modifications if not using the template

If you didn't use the hemlock template, create a new python3 jupyter notebook and enter the following in the first cell:

```python
from hemlock import push_app_context

push_app_context()
```

This sets up your hemlock environment, including an [application context](https://flask.palletsprojects.com/en/1.1.x/appcontext/), in the notebook.

### Code explanation

The first line simply imports `Page` and `Label` objects.

The next line, `p = Page(Label('<p>Hello, World!</p>'))`, creates a `Page` instance. A `Page` contains a list of 'questions' which it displays to participants. We set a page's questions by passing them as arguments to the constructor, or by setting the page's `questions` attribute, meaning that the following are equivalent:

```python
p = Page(Label('<p>Label 0</p>'), Label('<p>Label 1</p>'))
```

```python
p = Page()
p.questions = [Label('<p>Label 0</p>'), Label('<p>Label 1</p>')]
```

The `Page`'s question is a `Label`, although this is in some sense a misnomer because it only contains text. The first argument to `Label` is a string, written in html, which the `Label` displays on its page.

**Note.** If you don't like writing html, you can easily find Word to html converters online.

## Summary

In this part of the tutorial, you learned how to initialize a new hemlock project and create and preview a page.

In the next part of the tutorial, you'll learn how to run a hemlock application locally.
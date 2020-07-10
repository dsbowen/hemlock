# Your first project

In the previous part of the tutorial, you installed the necessary software to get started with hemlock.

By the end of this part of the tutorial, you'll be able to initialize a new hemlock project and create and preview hemlock survey pages.

## Initialize a new hemlock project

### From the hemlock template (recommended)

I recommend starting hemlock projects from the hemlock template:

```bash
$ hlk init my-first-project
```

This will 'clone' the template into a folder `my-first-project` and set up a virtual environment. Change into the project directory, activate the virtual environment, and install the requirements to run this project locally.

```bash
$ cd my-first-project
$ source hemlock-venv/bin/activate
$ pip install -r local-requirements.txt # or pip3 install -r local-requirements.txt
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
p.preview()
```

This opens a preview of your page in your browser.

Previewing works by creating temporary preview files. When you're done previewing your files, it's good practice to delete them:

```python
os.remove(*app.tmpfiles)
```

### Modifications if using WSL

If using Windows Subsystem for Linux (WSL), you'll need to specify your distribution as an environment variable. 

If using the hemlock template, open your local environment file:

```bash
$ code env/local-env.yml
```

And add the following line:

```yaml
WSL_DISTRIBUTION: Ubuntu # or other WSL distribution
```

If not using the hemlock template, export the environment variable:

```bash
$ export WSL_DISTRIBUTION=Ubuntu # or other WSL distribution
```

### Modifications if not using the template

If you're not using the hemlock template, create a new python3 jupyter notebook and enter the following in the first cell:

```python
from hemlock import push_app_context

app = push_app_context()
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

The `Page`'s question is a `Label`, although this is in some sense a misnomer because label objects only contains text. The first argument to `Label` is a string, written in html, which the label object displays on its page.

**Note.** If you don't like writing html, you can easily find Word to html converters online.

## Summary

In this part of the tutorial, you learned how to initialize a new hemlock project and create and preview a page.

In the next part of the tutorial, you'll learn how to run a hemlock application locally.
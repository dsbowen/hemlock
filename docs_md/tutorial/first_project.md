# Your first project

By the end of this part of the tutorial, you'll be able to initialize a new hemlock project and create and preview hemlock survey pages.

Click here to see what your <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.0/blackboard.ipynb" target="_blank">`blackboard.ipynb`</a> and <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.0/survey.py" target="_blank">`survey.py`</a> files should look like at the end of this part of the tutorial.

## Getting started

I've written setup pages for different operating systems (OS) below. You don't need everything in the setup page right now. First, read this list of things you need. Then, check out the setup page for your OS for download and installation instructions.

What you need to get started:

- Git and github (and a github authentication token)
- Python3 and pip3
- Hemlock-CLI
- Visual studio code
- Jupyter
- Google chrome

Check out the setup page for your OS:

- [Windows](../setup/win.md)
- [Windows Subsystem for Linux](../setup/wsl.md)
- [Mac](../setup/mac.md)
- [Linux](../setup/linux.md)

## Initialize a new hemlock project

Run the following, replacing `<my-github-username>` with your github username and`<my-github-token>` with your github authentication token:

```bash
$ hlk init my-first-project <my-github-username> <my-github-token>
```

For example, I would enter:

```bash
$ hlk init my-first-project dsbowen bts4rxpmw2x6tsy2qel1y7p5hwmhd7wxopmk5vsp
```

(This isn't my real authentication token!)

This will 'clone' the template into a folder `my-first-project`, initialize an eponymous github repository for your project, and set up a virtual environment.

Change into the project directory and check out the folder structure:

```bash
$ cd my-first-project
$ ls
```

!!! note
    You will only have to run `hlk init` once per project.

!!! error
    You may see an error message starting with *Cannot uninstall PyYAML*. To fix this, run:

    ```bash
    $ pip install --ignore-installed pyyaml
    ```

!!! note "If using Windows git bash"
    After changing into your project directory, set up your virtual environment:

    ```bash
    $ hlk setup-venv my-first-project
    ```

!!! note "If using WSL"
    You'll need to specify your distribution as an environment variable. Open the file which sets your local environment variables:

    ```bash
    $ code env.yaml
    ```

    And add the following line:

    ```yaml
    WSL_DISTRIBUTION: Ubuntu-20.04 # or other WSL distribution
    ```

    If you're not sure which distribution you have, run:

    ```bash
    $ explorer.exe .
    ```

    This will open a file explorer. At the top of the file explorer, you'll see:

    > `<my-wsl-distribution>\home\<my-wsl-username>\my-first-project`

    We're looking for `<my-wsl-distribution>`.

## Preview a page in jupyter notebook

Jupyter notebook is a great tool for iterating quickly on project designs. I recommend using it for most of your work. Open the jupyter dashboard with:

```bash
$ jupyter notebook
```

Jupyter will attempt to open the dashboard automatically in your browser. If this fails, the terminal window will show you links to the dashboard that you can manually copy and paste into your browser.

Open the file named `blackboard.ipynb`.

Change the kernel to `my-first-project` (in general, your project name). At the top of the notebook click Kernel >> Change kernel >> my-first-project.

Run the first cell (Shift + Enter) to set up the environment and application context. It's not important right now to understand exactly what it does.

Now, create your first hemlock page. In a new code cell below the first one, enter the following:

```python
from hemlock import Page, Label

p = Page(Label('<p>Hello, World!</p>'))
p.preview()
```

This opens a preview of your page in your browser.

Previewing works by creating temporary preview files. When you're done previewing your files, it's good practice to delete them:

```python
[os.remove(f) for f in app.tmpfiles if os.path.exists(f)]
```

## Code explanation

The first line simply imports `Page` and `Label` objects.

The next line, `p = Page(Label('<p>Hello, World!</p>'))`, creates a `Page` instance. A `Page` contains a list of 'questions' which it displays to participants. We can set a page's questions by passing them as arguments to the `Page` constructor. Alternatively, we can set a page's questions by setting the page's `questions` attribute, meaning that the following are equivalent:

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

<!-- ## Alternatively, from scratch

#### Initialize a new hemlock project

Create a folder for your project and change into it:

```bash
$ mkdir my-first-project
$ cd my-first-project
```

#### Set up your virtual environment

Create your virtual environment and activate it:

```bash
$ python3 -m venv hemlock-venv
```

Activate from git bash on Windows:

```bash
$ . hemlock-venv/scripts/activate
```

Activate from Windows command prompt:

```bash
$ hemlock-venv\scripts\activate.bat
```

Activate from Mac or WSL:

```bash
$ . hemlock-venv/bin/activate
```

Next, install hemlock and ipykernel:

```bash
$ pip install hemlock-survey ipykernel
```

Add your virtual environment to jupyter:

```bash
$ python3 -m ipykernel install --user --name=hemlock-venv
```

**Note.** You will only have to pip install hemlock and ipykernel and add hemlock-venv to jupyter once per project. However, you will have to activate your virtual environment every time you open a new terminal to work on this project. That is, suppose you close and re-open your terminal. You will have to change directory into your project folder and re-activate the virtual environment.

#### If using WSL

If using Windows Subsystem for Linux (WSL), you'll need to specify your distribution as an environment variable.

```bash
$ export WSL_DISTRIBUTION=Ubuntu-20.04 # or other WSL distribution
```

Make sure your `WSL_DISTRIBUTION` environment variable is set every time you open a terminal.

If you're not sure which distribution you have, run:

```bash
$ explorer.exe .
```

This will open a file explorer. At the top of the file explorer, you'll see:

> `<my-wsl-distribution>\home\<my-wsl-username>\my-first-project`

We're looking for `<my-wsl-distribution>`.

#### Preview a page in jupyter notebook

Jupyter notebook is a great tool for iterating quickly on project designs. I recommend using it for most of your work. Open the jupyter dashboard with:

```bash
$ jupyter notebook
```

Jupyter will attempt to open the dashboard automatically in your browser. If this fails, the terminal window will show you links to the dashboard that you can manually copy and paste into your browser.

Create a new notebook. In the upper right, click New >> hemlock-venv. 

Run the following in the first cell of your notebook:

```python
from hemlock import push_app_context

app = push_app_context()
```

This sets up the hemlock environment, including the application context. It's not important right now to understand exactly what it does.

Now, create your first hemlock page. In a new code cell below the first one, enter the following:

```python
from hemlock import Page, Label

p = Page(Label('<p>Hello, World!</p>'))
p.preview()
```

This opens a preview of your page in your browser.

Previewing works by creating temporary preview files. When you're done previewing your files, it's good practice to delete them:

```python
import os

[os.remove(tmpfile) for tmpfile in app.tmpfiles]
``` -->
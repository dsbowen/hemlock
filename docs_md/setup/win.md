# Windows setup

## Git and github

Git is a version control system, and github hosts code repositories. Together, they allow you to share and collaborate on hemlock projects. You will also need git to initialize hemlock projects with the hemlock template.

[Download git here](https://git-scm.com/download/win). You will be prompted to restart your computer.


We'll use the git bash terminal for this tutorial. Right click anywhere on your desktop and select 'Git Bash Here`. You should see a terminal window appear. Change to your home directory with:

```bash
$ cd ..
```

This command moves you up a directory.

**Note 1.** You don't type `$`; it simply indicates the beginning of a bash command.

**Note 2.** Always make sure you're in your home directory after you open the git bash terminal.

Verify your git installation:

```bash
$ git --version
git version x.xx.x.windows.1
```

Then, create a [github account here](https://github.com). Configure your github command line interface:

```bash
$ git config --global user.name <my-github-username>
$ git config --global user.email <my-github.user-email>
```

## Python3 and pip3

Python is hemlock's primary language. Pip allows you to install python packages, including hemlock and its command line interface, hemlock-cli.

You can [download the latest version of python here](https://www.python.org/downloads/). 

However, I recommend an earlier version, python3.6. [Download python3.6 here](https://www.python.org/ftp/python/3.6.8/python-3.6.8.exe). Why? Because heroku, my recommended method of app deployment, uses python3.6, meaning that if you develop in python3.7+ and deploy in python3.6, you may encounter compatibility issues.

**Make sure to click *Add Python to PATH* on the first page of the installer.**

Close and re-open your terminal window and enter:

```bash
$ which python
/c/Users/DBSpe/AppData/Local/Programs/Python/Python36-32/python
```

The line underneath `which python` is the location of your python executable, where <xx-xx> is your python version.

Change directories into this folder, for example:

```bash
$ cd appdata/local/programs/python/python<xx-xx>
```

Rename `python.exe` to `python3.exe`:

```bash
$ ls python.exe python3.exe
```

Verify your python installation:

```bash
$ python3 --version
Python 3.x.x
```

Upgrade pip:

```bash
$ python3 -m pip install --upgrade pip
```

Verify your pip installation:

```bash
$ pip3 --version
pip xx.x.x from c:\users\dbspe\appdata\local\programs\python\python36-32\lib\site-packages\pip (python 3.x)
```

Now, go back to your home directory (enter `cd ..` a few times).

## Hemlock-CLI

Hemlock's command line interface, hemlock-CLI, defines many useful commands for initializing, editing, and deploying hemlock projects. Download with:

```bash
$ pip install hemlock-cli
```

Verify your hemlock-cli installation:

```bash
$ hlk --version
hlk x.x.x
```

## Visual studio code

I recommend visual studio code for editing python files. [Download here](https://code.visualstudio.com/).

Close and re-open your terminal. Verify your VS code installation:

```bash
$ code --version
1.xx.x
```

## Jupyter

[Jupyter](https://jupyter.org/) allows you to quickly iterate on project designs. Install with pip:

```bash
$ pip install notebook
```

Close and re-open your terminal. Verify your jupyter installation:

```bash
$ jupyter --version
jupyter core     : x.x.x
jupyter-notebook : x.x.x
...
```

## Google chrome

Hemlock is developed and tested primarily on chrome. [Download chrome here](https://www.google.com/chrome/).

Verify that you can open it using the `webbrowser` command:

```bash
$ python3
>>> import webbrowser
>>> webbrowser.open('https://dsbowen.github.io/hemlock')
True
>>> exit()
```

You should see chrome open to the hemlock docs.

**Note.** `>>>` is where you enter python commands in the python interpreter.

## Chromedriver

Hemlock's custom debugging tool and survey view functions use [chromedriver](https://chromedriver.chromium.org/downloads). To use these features locally, you'll need to download chromedriver:

```bash
$ hlk setup win --chromedriver
```

Close and re-open your terminal. Verify your chromedriver installation:

```bash
$ which chromedriver.exe
/c/users/<my-windows-username>/webdrivers/chromedriver.exe
```

## Heroku

Heroku is an easy and inexpensive service for deploying web applications, including hemlock applications. [Download the command line interface here](https://devcenter.heroku.com/articles/heroku-cli).

Close and re-open your terminal. Verify your heroku-cli installation:

```bash
$ heroku --version
heroku/x.xx.x win32-x64 node-v11.14.0
```

Log into heroku:

```bash
$ heroku login
```
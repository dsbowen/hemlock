# Mac setup

These instructions were written for Mac OS 10.9.

## Open a terminal window

Hemlock requires you to use a terminal window for setting up, editing, and deploying hemlock projects. To open a terminal window, enter 'terminal' in spotlight search. Terminal commands are written in bash:

```bash
$ <my-bash-command>
```

**Note 1.** You don't type `$`; it simply indicates the beginning of a bash command.

**Note 2.** For this tutorial, always make sure to change to your home directory after you open your terminal.

## Python3 and pip3

Python is hemlock's primary language. Pip allows you to install python packages, including hemlock and its command line interface, hemlock-CLI.

You can [download the latest version of python here](https://www.python.org/downloads/). 

However, I recommend an earlier version, python3.6. [Download python3.6 here](https://www.python.org/ftp/python/3.6.8/python-3.6.8-macosx10.9.pkg). Why? Because heroku, my recommended method of app deployment, uses python3.6, meaning that if you develop in python3.7+ and deploy in python3.6, you may encounter compatibility issues.

**Make sure to click *Add Python to PATH* on the first page of the installer.**

Close and re-open your terminal window. Verify your python installation.

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
pip xx.x.x ...
```

## Hemlock-CLI

Hemlock's command line interface, hemlock-CLI, defines many useful commands for initializing, editing, and deploying hemlock projects. Download with:

```bash
$ pip install hemlock-cli
```

Verify your hemlockCLI installation:

```bash
$ hlk --version
hlk x.x.x
```

## Git and github

[Git](https://git-scm.com/) is a version control system, and [github](https://github.com/) hosts code repositories. Together, they allow you to share and collaborate on hemlock projects. You will also need git to initialize hemlock projects with the hemlock template.

You can install git using hemlock-CLI:

```bash
$ hlk setup mac --git
```

You will be prompted to create a github account.

Verify your git installation:

```bash
$ git --version
```

## Visual studio code

I recommend visual studio code for editing python files. [Download VS code here](https://code.visualstudio.com/).

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
$ hlk setup mac --chromedriver
```

Close and re-open your terminal. Verify your chromedriver installation:

```bash
$ which chromedriver
/users/<my-mac-username>/webdrivers/chromedriver
```

#### Chrome and chromedriver compatibility

As of 07/14/2020, `hlk setup mac --chromedriver` installs chromedriver for chrome 83. While chrome updates automatically, chromedriver does not. This means that you will encounter compatibility issues when chrome updates to version 84+. To fix this:

1. [Download the latest chromedriver here](https://chromedriver.chromium.org/downloads).
2. Put the chrome executable in `/users/<my-mac-username>/webdrivers/`.

Chromedriver should still be in your path, which you can verify:

```bash
$ which chromedriver
/users/<my-mac-username>/webdrivers/chromedriver
```

## Heroku

Heroku is an easy and inexpensive service for deploying web applications, including hemlock applications.

You can install heroku-CLI using hemlock-CLI:

```bash
$ hlk setup mac --heroku-cli
```

Verify your heroku-CLI installation:

```bash
$ heroku --version
heroku/x.xx.x mac-x64 node-vxx.xx.x
```
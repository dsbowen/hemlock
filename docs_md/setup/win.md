# Windows setup

These instructions were written for Windows 10.

## Git and github

Git is a version control system, and github hosts code repositories. Together, they allow you to share and collaborate on hemlock projects. You will also need git to initialize hemlock projects with the hemlock template.

You can find [git download and installation instructions here](https://git-scm.com/download/win).

We'll use the git bash terminal for this tutorial. Right click anywhere on your desktop and select 'Git Bash Here`. You should see a terminal window appear. Enter the following into your terminal:

```bash
$ cd
```

This moves you to your home directory. It's not important that you understand exactly what this means, but if you're dying to find out, [read this](https://towardsdatascience.com/basics-of-bash-for-beginners-92e53a4c117a).

**Note 1.** You don't type `$`; it simply indicates the beginning of a bash command.

**Note 2.** For this tutorial, always make sure to change to your home directory by entering `cd` after you open the git bash terminal.

Verify your git installation:

```bash
$ git --version
git version 2.27.0.windows.1
```

**Note 1.** The first line, `git --version`, is what you enter in the terminal. The second line, `git version 2.27.0.windows.1`, is the output. In general, lines that start with `$` are things you enter in your terminal; lines without `$` are the output of what you just entered.

**Note 2.** It's okay if you have a slightly different version of git. For example, your second line may read `git version 2.28.0.windows.1`.

Then, create a [github account here](https://github.com). Configure your github command line interface:

```bash
$ git config --global user.name <my-github-username>
$ git config --global user.email <my-github-user-email>
```

## Python3 and pip3

Python is hemlock's primary language. Pip allows you to install python packages, including hemlock itself. In this section, we're going to download and install python3 and pip3.

**Read everything until STOP before downloading or installing anything.**

You can [download the latest version of python here](https://www.python.org/downloads/). 

However, I recommend an earlier version, python3.6. [Download python3.6 here](https://www.python.org/ftp/python/3.6.8/python-3.6.8.exe). Then, click on the file you just downloaded to install it. 

Why do I recommend 3.6 instead of the latest version of python? Because heroku, my recommended method of app deployment, uses python3.6, meaning that if you develop in python3.7+ and deploy in python3.6, you may encounter compatibility issues.

**When you start the python installer, you'll see an *Add Python to PATH* option on the first page. Make sure to select this option.**

**STOP.**

Close and re-open your terminal window and enter:

```bash
$ which python
```

You should see a line print underneath `which python`. This is the location of your python executable (i.e. the file that runs python). On my computer, it looks like:

```bash
/c/Users/DBSpe/AppData/Local/Programs/Python/Python36-32/python
```

The python executable may be in a different location on your computer. In general, it'll look like:

```bash
<my-python-location>/python
```

We're going to change directories to that location (i.e. we're going to go to where the python executable is). On my computer, I would enter:

```bash
$ cd /c/Users/DBSpe/AppData/Local/Programs/Python/Python36-32
```

In general, you would enter:

```bash
$ cd <my-python-location>
```

**Note.** The line that printed under `which python` was `<my-python-location>/python`; you'll then enter `cd <my-python-location>`, *not* `cd <my-python-location>/python`.

Copy `python.exe` to `python3.exe`:

```bash
$ cp python.exe python3.exe
```

Verify your python installation:

```bash
$ python3 --version
Python 3.6.8
```

It's okay if you have a different version of python.

Next, upgrade pip:

```bash
$ python3 -m pip install --upgrade pip
```

Verify your pip installation:

```bash
$ pip3 --version
pip 20.1.1 from c:\users\dbspe\appdata\local\programs\python\python36-32\lib\site-packages\pip (python3.6)
```

Again, it's okay to have a slightly different version of pip.

Congratulations! You've installed python. Now return to your home directory:

```bash
$ cd
```

## Hemlock-CLI

Hemlock's command line interface, hemlock-CLI, defines many useful commands for initializing, editing, and deploying hemlock projects. Download with:

```bash
$ pip install hemlock-cli
```

Verify your hemlock-CLI installation:

```bash
$ hlk --version
hlk 0.0.10
```

## Visual studio code

I recommend visual studio code for editing python files. You can find [download and installation instructions for VS code here](https://code.visualstudio.com/).

Close and re-open your terminal. Verify your VS code installation:

```bash
$ code --version
1.47.2
17299e413d5590b14ab0340ea477cdd86ff13dafx64
```

## Jupyter

[Jupyter](https://jupyter.org/) allows you to quickly iterate on project designs. Install jupyter notebook with pip:

```bash
$ pip install notebook
```

Close and re-open your terminal. Verify your jupyter installation:

```bash
$ jupyter --version
jupyter core     : 4.6.3
jupyter-notebook : 6.0.3
qtconsole        : not installed
ipython          : 7.16.1
ipykernel        : 5.3.2
jupyter client   : 6.1.5
jupyter lab      : not installed
nbconvert        : 5.6.1
ipywidgets       : not installed
nbformat         : 5.0.7
traitlets        : 4.3.3
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

**Note.** `>>>` is where you enter python commands. This is called the 'python interpreter'.

## Chromedriver

Hemlock's custom debugging tool and survey view functions use [chromedriver](https://chromedriver.chromium.org/downloads). To use these features locally, you'll need to download chromedriver:

```bash
$ hlk setup win --chromedriver
```

Close and re-open your terminal. Verify your chromedriver installation:

```bash
$ which chromedriver.exe
```

The line underneath `which chromedriver.exe` is the location of your chromedriver executable. On my computer, it looks like:

```bash
/c/users/dbspe/webdrivers/chromedriver.exe
```

It's okay if your chromedriver executable is in a different location.

#### Chrome and chromedriver compatibility

As of 07/14/2020, `hlk setup win --chromedriver` installs chromedriver for chrome 83. While chrome updates automatically, chromedriver does not. This means that you will encounter compatibility issues when chrome updates to version 84+. To fix this:

1. [Download the latest chromedriver here](https://chromedriver.chromium.org/downloads).
2. Put the chrome executable in `C:\users\<my-windows-username>\webdrivers\`. For example, I would put my chromedriver executable in `C:\users\dbspe\webdrivers\`.

Chromedriver should still be in your path, which you can verify:

```bash
$ which chromedriver.exe
<my-chromedriver-location>/chromedriver.exe
```

## Heroku

Heroku is an easy and inexpensive service for deploying web applications (i.e. putting them online), including hemlock applications. You can find [download and installation instructions for the heroku command line interface (heroku-CLI) here](https://devcenter.heroku.com/articles/heroku-cli).

Close and re-open your terminal. Verify your heroku-CLI installation:

```bash
$ heroku --version
heroku/x.xx.x win32-x64 node-vxx.xx.x
```

Log into heroku:

```bash
$ heroku login
```
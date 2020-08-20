# Mac setup

These instructions were written for Mac OS 10.9.

## Open a terminal window

Hemlock requires you to use a terminal window for setting up, editing, and deploying hemlock projects. To open a terminal window, enter 'terminal' in spotlight search. Terminal commands are written in bash:

```bash
$ <my-bash-command>
```

**Note 1.** You don't type `$`; it simply indicates the beginning of a bash command.

**Note 2.** For this tutorial, always make sure to change to your home directory after you open your terminal. Do this by entering:

```bash
$ cd
```

## Xcode

Mac OS typically requires Xcode Command-line Tools. Install in your terminal:

```bash
$ xcode-select --install
```

Or from the <a href="https://apps.apple.com/us/app/xcode/id497799835" target="_blank">Mac app store</a>.

## Python3 and pip3

Python is hemlock's primary language. Pip allows you to install python packages, including hemlock and its command line interface, hemlock-CLI.

**Read everything until STOP before downloading or installing anything.**

You can [download the latest version of python here](https://www.python.org/downloads/). 

However, I recommend an earlier version, python3.6. [Download python3.6 here](https://www.python.org/ftp/python/3.6.8/python-3.6.8-macosx10.9.pkg). 

Why do I recommend 3.6 instead of the latest version of python? Because heroku, my recommended method of app deployment, uses python3.6, meaning that if you develop in python3.7+ and deploy in python3.6, you may encounter compatibility issues.

**When you start the python installer, you'll see an *Add Python to PATH* option on the first page. Make sure to select this option.**

**STOP.**

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

Hemlock's command line interface, hemlock-CLI, defines many useful commands for initializing, editing, and deploying hemlock projects. Install with:

```bash
$ pip install -U hemlock-cli
```

Verify your hemlock-CLI installation:

```bash
$ hlk --version
hlk, version x.x.xx
```

## Git and github

<a href="https://git-scm.com/" target="_blank">Git</a> is a version control system, and <a href="https://github.com/" target="_blank">github</a> hosts code repositories. Together, they allow you to share and collaborate on hemlock projects. You will also need git to initialize hemlock projects with the hemlock template.

Macs typically have git pre-installed, which you can verify:

```bash
$ git --version
git version 2.27.0.mac.1
```

If you don't have git, follow the [download and installation instructions here](https://git-scm.com/download/mac).

Then, create a [github account here](https://github.com). Configure your github command line interface:

```bash
$ git config --global user.name <my-github-username>
$ git config --global user.email <my-github-user-email>
```

For example, I would enter:

```bash
$ git config --global user.name dsbowen
$ git config --global user.email dsbowen@wharton.upenn.edu
```

Finally, you will need a personal access token to initialize hemlock applications with the hemlock command line interface.

**Read everything until STOP before creating your github token.**

1. Create a github token by following <a href="https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token" target="_blank">these instructions</a>.
2. When setting permissions (step 7), check 'repo'.
3. Copy your token and store it somewhere accessible. For example, I store my token in a file named `github_token.txt`.

**STOP.**

## Visual studio code

I recommend visual studio code for editing python files. [Download VS code here](https://code.visualstudio.com/).

Close and re-open your terminal. Verify your VS code installation:

```bash
$ code --version
1.xx.x
```

## Jupyter

<a href="https://jupyter.org/" target="_blank">Jupyter</a> allows you to quickly iterate on project designs. Install jupyter notebook with pip:

```bash
$ pip install -U notebook
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

Hemlock is developed and tested primarily on chrome. <a href="https://www.google.com/chrome/" target="_blank">Download chrome here</a>.

Verify that you can open it as follows:

```bash
$ python3
>>> import webbrowser
>>> webbrowser.open('https://dsbowen.github.io/hemlock')
True
>>> exit()
```

You should see chrome open to the hemlock docs.

**Note.** `>>>` is where you enter python commands in the python interpreter.

If you came here from the tutorial, you're now ready to return to it and get started with your first hemlock project. [Click here to go back to the First Project section of the tutorial](../tutorial/first_project.md).

## Chromedriver

Hemlock's custom debugging tool and survey view functions use <a href="https://chromedriver.chromium.org/downloads" target="_blank">chromedriver</a>. To use these features locally, you'll need to download chromedriver:

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

1. <a href="https://chromedriver.chromium.org/downloads" target="_blank">Download the latest chromedriver here</a>.
2. Put the chrome binary, `chromedriver`, in `/users/<my-mac-username>/webdrivers/`. For example, I would put my chromedriver binary in `/users/dsbowen/webdrivers/`.

Chromedriver should still be in your path, which you can verify:

```bash
$ which chromedriver
/users/<my-mac-username>/webdrivers/chromedriver
```

If you came here from the Debug section of the tutorial, you're now ready to return to it and run the debugger. [Click here to go back to the Debug section of the tutorial](../tutorial/debug.md).

## Heroku

Heroku is an easy and inexpensive service for deploying web applications (i.e. putting them online), including hemlock applications. <a href="https://signup.heroku.com/" target="_blank">Sign up for heroku here</a>.

You can install heroku-CLI using hemlock-CLI:

```bash
$ hlk setup mac --heroku-cli
```

Verify your heroku-CLI installation:

```bash
$ heroku --version
heroku/x.xx.x mac node-vxx.xx.x
```

**Note.** See <a href="https://github.com/heroku/legacy-cli/issues/1969" target="_blank">this github issue</a> if you experience a 'EACCES' error. *Do not* simply use `sudo`; this only masks issues you'll encounter later.

[Click here to return to the Deploy section of the tutorial](../tutorial/deploy.md).
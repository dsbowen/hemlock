# Linux setup

These instructions are based on the Ubuntu distribution of WSL.

## Python3 and pip3

Python is hemlock's primary language. Pip allows you to install python packages, including hemlock and its command line interface, hemlock-CLI. Many linux distributions come with python3.

Verify your python3 installation:

```bash
$ python3 --version
Python 3.x.x
```

If you don't have python3, [download it here](https://www.python.org/downloads/). I recommend python3.6. Why? Because heroku, my recommended method of app deployment, uses python3.6, meaning that if you develop in python3.7+ and deploy in python3.6, you may encounter compatibility issues. Make sure python3 is in your path.

Upgrade pip:

```bash
$ python3 -m pip install --upgrade pip
```

Verify your pip installation:

```bash
$ pip3 --version
pip xx.x.x ...
```

#### pip versus pip3

You'll install several python packages using pip. Conventionally, the command to install these is:

```bash
$ pip install <my-requested-package>
```

You may need to replace this with:

```bash
$ pip3 install <my-requested-package>
```

Many hemlock-CLI commands assume you can pip install with `pip3`.

## Hemlock-CLI

Hemlock's command line interface, hemlock-CLI, defines many useful commands for initializing, editing, and deploying hemlock projects. Download with:

```bash
$ pip install hemlock-cli
```

Verify your hemlock-CLI installation:

```bash
$ hlk --version
hlk x.x.x
```

## Git and github

[Git](https://git-scm.com/) is a version control system, and [github](https://github.com/) hosts code repositories. Together, they allow you to share and collaborate on hemlock projects. You will also need git to initialize hemlock projects with the hemlock template.

[Find installation instructions for git here](https://git-scm.com/download/linux).

Verify your git installation:

```bash
$ git --version
git version x.xx.x.windows.1
```

Then, create a [github account here](https://github.com). Configure your github command line interface:

```bash
$ git config --global user.name <my-github-username>
$ git config --global user.email <my-github-user-email>
```

Finally, you will need a personal access token to initialize hemlock applications with the hemlock command line interface (more on this later). Create a token by following [these instructions](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token). When setting permissions (step 7), check 'repo'. Copy your token and store it somewhere accessible. For example, I store my token in a file named `github_token.txt`.

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

## Chromedriver

Hemlock's custom debugging tool and survey view functions use [chromedriver](https://chromedriver.chromium.org/downloads). To use these features locally, you'll need to download chromedriver:

```bash
$ hlk setup linux --chromedriver
```

Close and re-open your terminal. Verify your chromedriver installation:

```bash
$ which chromedriver
/home/<my-linux-username>/webdrivers/chromedriver
```

#### Chrome and chromedriver compatibility

As of 07/14/2020, `hlk setup linux --chromedriver` installs chromedriver for chrome 83. While chrome updates automatically, chromedriver does not. This means that you will encounter compatibility issues when chrome updates to version 84+. To fix this:

1. [Download the latest chromedriver here](https://chromedriver.chromium.org/downloads).
2. Put the chrome executable in `/home/<my-linux-username>/webdrivers/`.

Chromedriver should still be in your path, which you can verify:

```bash
$ which chromedriver
/home/<my-linux-username>/webdrivers/chromedriver
```

## Heroku

Heroku is an easy and inexpensive service for deploying web applications, including hemlock applications.

You can install heroku-CLI using hemlock-CLI:

```bash
$ hlk setup linux --heroku-cli
```

Verify your heroku-CLI installation:

```bash
$ heroku --version
heroku/x.xx.x linux-x64 node-vxx.xx.x
```
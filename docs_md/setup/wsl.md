# Windows Subsystem for Linux (WSL) setup

These instructions were written for Windows 10.

Why WSL? The main reason I use WSL is that Windows OS doesn't have a fork (only a spoon), which means you'll need WSL if you want to run Redis. You can find [download instructions for WSL here](https://docs.microsoft.com/en-us/windows/wsl/install-win10). Either WSL 1 or 2 should work.

After you've installed WSL, open a terminal window (WIN + R, then enter e.g. 'ubuntu2004'. You may be prompted to create a username and password.

## Python3 and pip3

Python is hemlock's primary language. Pip allows you to install python packages, including hemlock and its command line interface, hemlock-CLI.

Most WSL distributions come with python3. Verify your python installation with:

```
$ python3
Python 3.x.x
```

If you don't have python intalled on your WSL distribution, [download python here](https://www.python.org/downloads/). I recommend python3.6, rather than the latest version. Why? Because heroku, my recommended method of app deployment, uses python3.6, meaning that if you develop in python3.7+ and deploy in python3.6, you may encounter compatibility issues.

Update your package lists:

```bash
$ sudo apt-get update
```

Install pip3:

```bash
$ sudo apt install -f -y python3-pip
```

Respond 'Yes' if asked whether you want to restart services automatically.

Verify your pip3 installation:

```bash
$ pip3 --version
pip x.x.x from /usr/lib/python3/dist-packages (python 3.x)
```

You'll also need the ability to create virtual environments:

```bash
$ apt install -f -y python3-venv
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

**Note.** Make sure to download the Windows version, not the Linux version.

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

**Note.** If this doesn't work, it's probably because the chrome executable isn't in your path. Run the following:

```bash
$ hlk setup wsl --chrome
```

Close and re-open your terminal. Verify your `BROWSER` variable:

```bash
$ echo $BROWSER
/mnt/c/program files (x86)/google/chrome/application/chrome.exe
```

Now try again to open the webbrowser.

## Chromedriver

Hemlock's custom debugging tool and survey view functions use [chromedriver](https://chromedriver.chromium.org/downloads). To use these features locally, you'll need to download chromedriver:

```bash
$ hlk setup wsl --chromedriver
```

Close and re-open your terminal. Verify your chromedriver installation:

```bash
$ which chromedriver
/mnt/c/users/<my-windows-username>/webdrivers/chromedriver
```

#### Chrome and chromedriver compatibility

As of 07/14/2020, `hlk setup wsl --chromedriver` installs chromedriver for chrome 83. While chrome updates automatically, chromedriver does not. This means that you will encounter compatibility issues when chrome updates to version 84+. To fix this:

1. [Download the latest chromedriver here](https://chromedriver.chromium.org/downloads). Windows version, not Linux version.
2. Put the chrome executable in `C:\users\<my-windows-username>\webdrivers\`.
3. Rename the executable from `chromedriver.exe` to `chromedriver`.

Chromedriver should still be in your path, which you can verify:

```bash
$ which chromedriver
/mnt/c/users/<my-windows-username>/webdrivers/chromedriver
```

## Heroku

[Heroku](https://devcenter.heroku.com/articles/heroku-cli) is an easy and inexpensive service for deploying web applications, including hemlock applications.

If using hemlock-CLI, you can install and configure the heroku command line interface with:

```bash
$ hlk setup wsl --heroku-cli
```

This will prompt you to create and log in to a heroku account.

Verify your heroku-CLI installation:

```bash
$ heroku --version
heroku/x.xx.x linux-x64 node-vxx.xx.x
```
# Setup

## Essential

1. [Google Chrome](https://www.google.com/chrome/).
2. [Python3 and pip3](https://www.python.org/downloads/), recommended version 3.6. This is hemlock's primary language.
3. A way to open and edit python files. Recommended [Visual Studio Code](https://code.visualstudio.com/).

## pip versus pip3

You'll install several python packages using pip. Conventionally, the command to install these is:

```bash
$ pip install <my-requested-package>
```

**Note 1.** You don't type `$`; this just means 'the start of a command in your terminal window'.

**Note 2.** Depending on your operating system, you may need to replace `pip` with `pip3`.

```bash
$ pip3 install <my-requested-package>
```

If one doesn't work, try the other.

#### Windows users

I recommend installing [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install-win10) with the Ubuntu Linux distribution. Either WSL 1 or WSL 2 should work. This comes with python and pip.

After you've installed Ubuntu, open a terminal window (WIN + R, then enter 'ubuntu\<xxxx\>', where \<xxxx\> is your version of ubuntu, e.g. 'ubuntu2004'). You will be prompted to create a username and password.

Verify your python installation with:

```
$ python3
Python 3.6.x
```

**Note.** You don't type `$` in the terminal window; it simply denotes the beginning of a terminal command.

Update your package lists with:

```bash
$ sudo apt-get update
```

Install pip3 with:

```bash
$ sudo apt install -f -y python3-pip
```

Respond 'Yes' if asked whether you want to restart services automatically.

Verify your pip3 installation:

```bash
$ pip3 --version
pip x.x.x from /usr/lib/python3/dist-packages (python 3.6)
```

**Note.** When installing python packages, use `pip3` instead of `pip`:

```bash
$ pip3 install <the-package-I-want> # instead of pip install <the-package-I-want>
```

Finally, I recommend setting your `BROWSER` environment variable after installing hemlock-CLI (see below).

## Recommended

The following aren't necessary to use hemlock, but they will make your life easier. The rest of the tutorial assumes you have these.

### Hemlock-CLI

Use pip to install the hemlock command line interface (CLI).

```bash
$ pip install hemlock-cli
```

Verify your installation:

```bash
$ hlk --version
hlk, version x.x.x
```

### Chrome

I assume most users will access your hemlock applications through Google chrome.

##### If using WSL

To set chrome as your default browser from WSL, run:

```bash
$ hlk setup win --chrome
```

Close and re-open your terminal, then verify your `BROWSER` variable:

```bash
$ echo $BROWSER
/mnt/c/program files (x86)/google/chrome/application/chrome.exe
```

##### If not using WSL

You will need a `BROWSER` environment variable, which should be set for you automatically.

### Git

Git and github are version control tools for sharing, downloading, and collaborating on software, including hemock projects. 

##### If using WSL

Run:

```bash
$ hlk setup win --git
```

##### If not using WSL


Download [git here]((https://git-scm.com/downloads), and register for [github here](https://github.com/).

### Jupyter

Jupyter allows you to quickly iterate on project designs. For no good reason, I personally use Jupyter Notebook, not JupyterLab. [Download here]((https://jupyter.org/install).

activate venv
install local requirements
add venv to jupyter using this command
open notebook
kernel ==> change kernel to hemlock-venv
(see what happens with Lance)
https://www.google.com/url?q=https://towardsdatascience.com/create-virtual-environment-using-virtualenv-and-add-it-to-jupyter-notebook-6e1bf4e03415&sa=D&source=hangouts&ust=1594571729871000&usg=AFQjCNGWbqMRGF1tjs92L2g_Ja999wp53Q
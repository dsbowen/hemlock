# Setup

## Essential

1. Google Chrome. [Download here](https://www.google.com/chrome/).
2. Python3 and pip3, recommended version 3.6. This is hemlock's primary language. [Download python here](https://www.python.org/downloads/).
3. A way to open and edit python files; recommended Visual Studio Code. [Download here](https://code.visualstudio.com/).

## pip versus pip3

You'll install several python packages using pip. Conventionally, the command to install these is:

```bash
$ pip install <my-requested-package>
```

**Note 1.** You don't type `$`; this just means 'the start of a command in your terminal window'.

**Note 2.** Depending on your operating system, you may need to replace `pip` with `pip3`:

```bash
$ pip3 install <my-requested-package>
```

If one doesn't work, try the other.

#### Windows users

I recommend installing Windows Subsystem for Linux (WSL) with the Ubuntu Linux distribution. Either WSL 1 or WSL 2 should work. This comes with python and pip. [Download instructions for WSL here](https://docs.microsoft.com/en-us/windows/wsl/install-win10).

After you've installed Ubuntu, open a terminal window (WIN + R, then enter 'ubuntu\<xxxx\>', where \<xxxx\> is your version of ubuntu, e.g. 'ubuntu2004'). You will be prompted to create a username and password.

Verify your python installation with:

```
$ python3
Python 3.6.x
```

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

[Download git here](https://git-scm.com/downloads), and [register for github here](https://github.com/).

### Jupyter

Jupyter allows you to quickly iterate on project designs. For no good reason, I personally use Jupyter Notebook, not JupyterLab. [Download jupyter here](https://jupyter.org/install).
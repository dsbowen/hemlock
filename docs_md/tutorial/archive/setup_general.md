# Setup

Here are the prerequisites I recommend to take advantage of the full range of tools Hemlock offers. Unless otherwise specified, I recommend you download the latest stable version of the following:

**Essential**

1. *Python3 and pip3*. Python is Hemlock's primary language. pip allows you to install Python packages, including Hemlock itself. I recommend [Python3.6](https://www.python.org/downloads/release/python-366/), the version you will use for Heroku deployment (see below). Additionally, you should be able to create [virtual environments](https://docs.python.org/3/library/venv.html).
2. *Code editor*. I work in [Visual Studio (VS) Code](https://code.visualstudio.com/download) with the [Remote-WSL](https://code.visualstudio.com/docs/remote/wsl) extension, but any code editor will do.

**Strongly recommended**

1. *Heroku and Heroku-CLI*. [Heroku](https://heroku.com/) is an inexpensive and accessible service for deploying web applications. The Hemlock command line interface builds on the [Heroku command line interface (CLI)](https://devcenter.heroku.com/articles/heroku-cli).
2. *Git*. [Git](https://git-scm.com/) is a version control system which I use to 'push' applications to Heroku. Relatedly, I recommend [Github](https://github.com/) for backing up Hemlock projects and sharing them with collaborators.

With the above software, you are ready to create, share, and deploy Hemlock projects.

The software below is encouraged for debugging, file storage, and Redis testing. They are not essential. If you're eager to get started with Hemlock, you can come back to these if and when you need them.

**Encouraged**

1. *Google Chrome and Chromedriver*. Hemlock's custom debugging tool requires [Google Chrome](https://www.google.com/chrome/) and [Chromedriver](https://chromedriver.chromium.org/downloads) to run locally.
2. *Google Cloud and Cloud SDK*. Hemlock easily integrates with [Google Cloud](https://cloud.google.com/) for storing statics (such as images to display during a survey) and user uploaded files. The Hemlock command line interface builds on [Cloud Software Development Kit (SDK)](https://cloud.google.com/sdk/).

**Advanced**

1. *Redis*. Hemlock seamlessly interfaces with [Redis](https://redis.io) to run complex background processes during surveys. Redis runs natively on Mac and Linux. For Windows users, I recommend [Ubuntu](https://ubuntu.com/) on [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install-win10). 

## Instructions for Windows

Overview:

1. Install [Google Chrome](https://www.google.com/chrome/).
2. Install Ubuntu and Windows Subsystem for Linux (WSL).
3. Install Python3 and pip3 on Ubuntu.
4. Use pip3 to install Hemlock-CLI.
5. Use Hemlock-CLI to install other recommended software (Visual Studio Code, Google Chrome, etc.)

### Ubuntu and WSL

Follow the [Microsoft documentation](https://docs.microsoft.com/en-us/windows/wsl/install-win10) to enable WSL and install the latest version of Ubuntu.

Open an Ubuntu terminal (WIN + R, then enter 'ubuntu'). You will be prompted to create a username and password.

### Python3 and pip3

Ubuntu should include Python3.6. Verify your Python installation with:

```bash
$ python3 --version
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

Finally, verify pip3 installation:

```bash
$ pip3 --version
pip x.x.x from /usr/lib/python3/dist-packages (python 3.6)
```

### Hemlock-CLI

pip install the Hemlock command line interface (CLI):

```bash
$ pip3 install hemlock-cli
```

Verify `hemlock-cli` installation:

```bash
$ hlk --version
hlk, version x.x.x
```

### Recommended software

Install other Hemlock utilities and recommended software with `hlk setup win [options]`. The options specify which recommended software tools you want to download. To download all recommended software, run:

```bash
$ hlk setup --all
```

This is equivalent to:

```bash
$ hlk setup --vscode --heroku-cli --git --chromedriver --cloud-sdk
```

VS Code and Cloud SDK will open setup executables automatically. Follow the directions when prompted.

You will also be prompted to login or create accounts for Heroku-CLI, Git, and Cloud SDK.

To verify the installations, close and re-open the Ubuntu terminal, then enter:

```bash
$ code --version
$ heroku --version
$ git --version
$ chromedriver --version
$ gcloud --version
```

Finally, if you are using Cloud SDK, you will need the alpha component:

```bash
$ gcloud components install alpha
```

## Instructions for Mac and Linux in progress
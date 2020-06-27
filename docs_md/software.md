# Software

Find installations instructions for:

1. [Windows](win_setup.md)
2. Mac and Linux in progress

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
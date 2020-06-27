# Instructions for Windows

Overview:

1. Install [Google Chrome](https://www.google.com/chrome/).
2. Install Ubuntu and Windows Subsystem for Linux (WSL).
3. Install Python3 and pip3 on Ubuntu.
4. Use pip3 to install Hemlock-CLI.
5. Use Hemlock-CLI to install other recommended software (Visual Studio Code, Chromedriver, etc.)

## Ubuntu and WSL

Follow the [Microsoft documentation](https://docs.microsoft.com/en-us/windows/wsl/install-win10) to enable WSL and install the latest version of Ubuntu.

Open an Ubuntu terminal (WIN + R, then enter 'ubuntu'). You will be prompted to create a username and password.

## Python3 and pip3

Ubuntu should include Python3.6. Verify your Python installation with:

```bash
$ python3 --version
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

Finally, verify pip3 installation:

```bash
$ pip3 --version
pip x.x.x from /usr/lib/python3/dist-packages (python 3.6)
```

## Hemlock-CLI

pip install the Hemlock command line interface (CLI):

```bash
$ pip3 install hemlock-cli
```

Verify `hemlock-cli` installation:

```bash
$ hlk --version
hlk, version x.x.x
```

## Recommended software

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

## Chromedriver note

The Chromedriver version downloaded by the Hemlock CLI is compatible with Chrome 83. While Chrome upgrades automatically, Chromedriver does not. When Chrome updates, you will experience errors due to Chrome-Chromedriver incompatibility.

To fix this, you will need to manually upgrade Chromedriver:

1. Download the appropriate Chromedriver version from <https://chromedriver.chromium.org/downloads>.
2. Rename the Chromedriver executable from `chromedriver.exe` to `chromedriver`.
3. Store the Chromedriver executable in `C:/users/my-username/webdrivers/`, replacing `my-username` with your Windows username.
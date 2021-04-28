# Setup

## Preliminary steps

=== "Windows"
    You're good to go!

=== "MacOS"
    MacOS typically requires Xcode Command-line Tools. Open a terminal window (enter "terminal" in spotlight seearch) and enter:

    ```bash
    $ xcode-select --install
    ```

    !!! note
        Don't type `$`, just `xcode-select --install`.

    Or install from the <a href="https://apps.apple.com/us/app/xcode/id497799835" target="_blank">Mac app store</a>.

=== "Linux"
    You may have to update your package lists:

    ```bash
    $ sudo apt-get update
    ```

=== "WSL"
    First, make sure you're on WSL2, not WSL1.

    Update your package lists:

    ```bash
    $ sudo apt-get update
    ```

    Install X server, which allows you to access the web and open web browsers from inside WSL.

    Download and install [VcXsrv](https://sourceforge.net/projects/vcxsrv/) **in Windows**. Make sure you allow X server to access public networks. If you accidentally didn't, see <a href="https://skeptric.com/wsl2-xserver/" target="_blank">here</a> and <a href="https://github.com/cascadium/wsl-windows-toolbar-launcher#firewall-rules" target="_blank">here</a> for troubleshooting.

    Finally, set the `DISPLAY` environment variable for the X server by adding these lines to the bottom of your `.profile` or `.bashrc` file:

    ```
    export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2; exit;}'):0.0
    export LIBGL_ALWAYS_INDIRECT=1
    ```

    Verify that you've set the DISPLAY variable correctly:

    ```bash
    $ echo $DISPLAY
    172.19.192.1:0.0
    ```

    If that didn't work, close and re-open your terminal, then run `echo $DISPLAY` again.

    To run the X server, run `xlaunch.exe` from the VcSrc folder in Program Files (or use the desktop icon if you have it). Keep the default settings *except make sure to select "Disable access control"*.

## Getting started

You only need 3 things to get started with hemlock:

1. Git and github
2. Anaconda
3. Hemlock-CLI

### Git and Github

#### Git

Git is a version control system, and github hosts code repositories. Together, they allow you to share and collaborate on hemlock projects.

You can find <a href="https://git-scm.com/download/">git download and installation instructions here</a>.

Now open a terminal window. On Windows, right-click anywhere on your desktop and select "Git Bash Here". On Mac, enter "terminal" in spotlight search.

Enter the following in your terminal to verify your git installation:

```bash
$ git --version
```

!!! note
    You don't type `$`. This just indicates the beginning of a bash command. Just type `git --version`.

Underneath `git --version` you should see a line like `git version 2.25.1`.

#### Github

Now create a <a href="https://github.com" target="_blank">github account here</a>. Configure your github command line interface:

```bash
$ git config --global user.name YOUR-GITHUB-USERNAME
$ git config --global user.email YOUR-GITHUB-USER-EMAIL
```

For example, I would enter:

```bash
$ git config --global user.name dsbowen
$ git config --global user.email dsbowen@wharton.upenn.edu
```

**Read everything until STOP before creating your github token.**

Finally, you will need a personal access token to initialize hemlock applications with the hemlock command line interface (more on this later).

1. Create a github token by following <a href="https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token" target="_blank">these instructions</a>.
2. When setting permissions (step 7), check "repo".
3. Copy your token and store it somewhere accessible. For example, I store my token in a file named `github_token.txt`.

**STOP.**

### Anaconda

Anaconda is a distribution of python (hemlock's primary programming language) that comes with several handy tools.

=== "Windows, MacOS, Linux"
    **Read everything before STOP before downloading and installing Anaconda.**

    Install the <a href="https://www.anaconda.com/products/individual" target="_blank">Individual Edition</a>.

    Check the box next to "Add Anaconda to PATH" when prompted. The installer will caution you against it but ignore the warning.

    **STOP.**

=== "WSL"
    Follow <a href="https://gist.github.com/kauffmanes/5e74916617f9993bc3479f401dfec7da" target="_blank">these instructions</a>. Make sure to respond "yes" when asked if you want to add anaconda to `PATH`.

    ??? warning "Do not install VS code through anaconda"
        <a href="https://code.visualstudio.com/docs/remote/wsl-tutorial" target="_blank">See here</a> if you want to use VS code in WSL.

To verify your installation, open a terminal window and enter:

```bash
$ which python
```

This should print a path with "anaconda" in it, e.g., `/home/dsbowen/anaconda3/bin/python`.

We'll edit hemlock projects using jupyter lab. Verify that you can open jupyter lab with:

```bash
$ jupyter lab
```

This should open jupyter lab in a browser window.

??? error "ImportError: no module found named win32api"
    If you experience this error when opening jupyter lab, simply install win32api:

    ```bash
    $ pip install pywin32
    ```

    Try opening jupyter lab again. You may have to close and re-open your terminal window.

### Hemlock-CLI

Hemlock's command line interface, hemlock-CLI, defines many useful commands for initializing, editing, and deploying hemlock projects. Install it with:

```bash
$ pip install -U hemlock-cli
```

Verify your installation with:

```bash
$ hlk --version
```

This should print a line like `hlk, version 0.0.21`.

!!! success "You're ready!"
    You now have everything you need to get started with hemlock. You can finish the setup later.

## Google chrome and chromedriver

You'll need google chrome and chromedriver to run hemlock's custom debugger.

### Google chrome

=== "Windows and MacOS"
    <a href="https://www.google.com/chrome/" target="_blank">Download chrome here</a>.

=== "Linux and WSL"
    Download chrome with:

    ```bash
    $ hlk setup linux --chrome
    ```

Verify that you can open it:

```
$ python -m webbrowser https://dsbowen.github.io
```

You should see chrome open to my github.io page.

### Chromedriver

Hemlock's custom debugging tool uses selenium python with chromedriver. 

**Read everything until STOP before doing anything.**

Download chromedriver with:

```bash
$ hlk setup YOUR-OS --chromedriver
```

Replace `YOUR-OS` with `win`, `mac`, or `linux` depending on your operating system (WSL users should use `linux`).

??? error "'curl' is not recognized as an internal or external command"
    If you get this error, <a href="https://www.tecmint.com/install-curl-in-linux/" target="_blank">see here to install `curl`</a> then try the command again.

The command will ask you to copy the appropriate chromedriver download URL from <a href="https://chromedriver.chromium.org/downloads" target="_blank">here</a> into your terminal window.

1. Under "Current Releases", click the link for your version of chrome. You should see zip files like, `chromedriver_linux64.zip`.
2. Right-click on the appropriate `zip` file for your OS and copy the link address.
3. Paste the link address in your terminal window and hit Enter.

**STOP.**

Verify your chromedriver installation:

```bash
$ chromedriver --version
```

This should print a line like `ChromDriver 88.0.4324.96 ...`.

??? error "Nothing prints under `chromedriver --version`"
    First, verify that chromedriver was downloaded.

    === "Windows and Mac"
        Enter:

        ```bash
        $ ls ~/webdrivers
        ```

        This should print `chromedriver` or `chromedriver.exe`. If nothing prints, chromedriver wasn't downloaded. Download it manually <a href="https://chromedriver.chromium.org/downloads" target="_blank">here</a>.

    === "Linux and WSL"
        Enter:

        ```bash
        $ ls /usr/bin/chromedriver
        ```

        This should print out `/usr/bin/chromedriver`. If nothing prints, chromedriver wasn't downloaded. Download it manually <a href="https://chromedriver.chromium.org/downloads" target="_blank">here</a>.

    Once you've verified your chromedriver download, the most likely issue is that it isn't in your `PATH`. Look up how to modify your path and add `/webdrivers/chromedriver` (Windows and Mac) or `/usr/bin/chromedriver` (Linux and WSL) to your path.

!!! warning "Chrome and chromedriver compatibility"
    Google chrome may automatically update but chromedriver will not. If you encounter a compatibility error in the future, simply repeat the above instructions.

## Heroku

Heroku is an easy and inexpensive service for deploying web applications (i.e., putting them online), including hemlock applications.

First, sign up for heroku <a href="https://signup.heroku.com/" target="_blank">here</a>.

=== "Windows"
    Download and install the heroku command line interface (heroku-CLI) following <a href="https://devcenter.heroku.com/articles/heroku-cli" target="_blank">these instructions</a>.

    Close and re-open your terminal.

=== "MacOS, Linux, WSL"
    Install the heroku-CLI with:

    ```bash
    $ hlk setup YOUR-OS --heroku-cli
    ```

    Replace `YOUR-OS` with `mac` or `linux` (WSL users should use `linux`).

    This will prompt you to log in to your heroku account.

Verify your heroku-CLI installation:

```bash
$ heroku --version
```

This should print a line like `heroku/7.49.1...`.

??? error "EACCES error"
    See <a href="https://github.com/heroku/legacy-cli/issues/1969" target="_blank">this github issue</a> if you experience a 'EACCES' error. *Do not* simply use `sudo`; this only masks issues you'll encounter later.
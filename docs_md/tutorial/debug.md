# Debugging

In the previous part of the tutorial, you implemented the responder branch.

By the end of this part of the tutorial, you'll be able to use hemlock's debugging tool to make sure your app is running smoothly.

## Why a custom debugging tool?

In the early days of hemlock, I coded a study in which I asked participants to estimate the ages of people in photographs. I used a submit function to change their data from strings to integers. Everything was running smoothly until one mischievous participant entered 'twenty-seven', breaking my survey and sending me home in a fit of rage.

Since then, I've rewritten my submit functions to be more fault tolerant. If you run

```python
from hemlock import Input, Submit

Submit.data_type(Input(data='twenty-seven'), int)._submit().data
```

it doesn't break; it simply converts the data to `None`.

But that wasn't good enough. We often underestimate just how strangely participants will respond to our studies in ways that we can't foresee.

To mitigate this problem, I wrote a custom debugging tool for hemlock. The tool sends an *AI participant* through your survey to check things out. 'AI participant' is a bit of a misnomer; if anything, it's an artificially stupid participant. It clicks random buttons, enters random things into inputs and text boxes, drags range sliders to random values; basically stress testing your code.

## Setup

To run hemlock's custom debugging tool locally, you'll need [Google Chrome](https://www.google.com/chrome/) and [Chromedriver](https://chromedriver.chromium.org/downloads).

### With hemlock-CLI on WSL

To install chromedriver, run:

```bash
$ hlk setup --chromedriver
```

This downloads a version of Chromdriver compatible with Chrome 83 and adds puts it here: `C:\Users\<my-windows-username>\webdrivers\chromedriver`. It also adds an environment variable for easy access in python. 

To verify your installation, close and re-open your terminal and run:

```bash
$ which chromedriver
/mnt/c/users/<my-windows-username>/chromedriver
```

**Note.** The Chromedriver version downloaded by the Hemlock CLI is compatible with Chrome 83. While Chrome upgrades automatically, Chromedriver does not. When Chrome updates, you will experience errors due to Chrome-Chromedriver incompatibility.

To fix this, you will need to manually upgrade Chromedriver:

1. Download the appropriate Chromedriver version from <https://chromedriver.chromium.org/downloads/>.
2. Store the Chromedriver executable in `C:/users/<my-windows-username>/webdrivers/`.
3. Rename the Chromedriver executable from `chromedriver.exe` to `chromedriver`.


### Without hemlock-CLI

1. Download the appropriate version of Chromedriver from <https://chromedriver.chromium.org/downloads/>.
2. Add the Chromedriver executable to your PATH (it's easy to find a guide for this online). 
3. If working in WSL, rename the Chromedriver executable from `chromedriver.exe` to `chromedriver`. (It took me hours of Googling + trial end error to figure this out).

Verify your installation, close and re-open your terminal and run:

```bash
$ which chromedriver
/path/to/my/chromedriver
```

## Basic syntax

Open your jupyter notebook and run the following:

```python
from hemlock import Debug, Input, Page
from hemlock.tools import chromedriver

driver = chromedriver()

p = Page(Debug.send_keys(Input(), 'hello world'))
p.debug_functions.pop()
p.preview(driver)._debug(driver)
```

First, we use `chromedriver` to open Chromedriver with [selenium python](https://selenium-python.readthedocs.io/).

Next, we create a page, attaching a debug function to an input question on the page. Like the other functions you've seen, `Debug.send_keys(Input(), 'hello world')` attaches a `send_keys` debug function to the `Input()` with an argument `'hello world'` and returns the input question to which it is attached.

We then pop the last debug function from the page we created. Why? By default, pages have two debug functions. The first executes its questions' debug methods in random order; as if the participant were randomly jumping between questions on a page. The second debug function randomly clicks a forward or back button (if it exists), or refreshes the page. Popping the debug function prevents the debugger from navigating, which is often a good idea in preview mode.

Finally, we run the debug function. You'll notice it enters 'hello world' in the input.

## Default debug functions

We can attach debug functions to pages or questions. Most questions have a default debug function. For example, input questions have a default debug function which sends random ASCII characters to the input.

However, sometimes we need to attach additional debug functions. For example, our study begins by asking participants to enter their date of birth in `mm/dd/yyyy` format. If you wait for the default debug function to randomly enter a string which matches that pattern, you might not end up running your study before Trump releases his tax returns.

Instead, we'll use something like:

```python
Page(Debug.send_keys(
    Input('<p>Enter your date of birth.</p>'), 
    '10/26/1992', p_exec=.8
))
```

You can pass `p_exec` as a keyword argument to any debug function. This is the probablity that the debug function will execute. This is useful because we want the debugger to occasionally enter something random into the date of birth input to see if anything breaks.

`send_keys` is just one of many pre-built [debug functions](../debug_functions.md).

## Custom debug functions

We won't need custom debug functions for our survey, but you may need them elsewhere. Creating custom debug function is similar to creating custom compile, validate, etc. functions, with one important difference: while the functions you've seen take their parent as their first argument, debug functions take a selenium webdriver as their first argument and their parent as their second argument:

```python
@Debug.register
def f(driver, parent):
    # debug something
```

## Debugging our app

Our app can be debugged largely with default debug functions. The exceptions are, 1) the date of birth input, 2) the comprehension check, 3) proposals and responses.

### Date of birth

Modify `survey.py` as follows:

```python
...

@route('/survey')
def start():
    demographics_page = Page(
        Debug.send_keys(
            Submit.record_age(Validate.validate_date_format(Input(
                '<p>Enter your date of birth.</p>',
                placeholder='mm/dd/yyyy',
                var='DoB', data_rows=-1
            ))),
            '10/26/1992', p_exec=.8
        ),
        ...
```

### Comprehension checks

Because there is no attempt limit for our comprehension check, unless we tell the debugger to enter the correct answers, it's going to keep looping back to the instructions page.

```python
...

@Compile.register
def random_proposal(check_page, accept):
    ...
    # add submit functions to verify that the response was correct
    check_page.questions[1].submit_functions.clear()
    Debug.send_keys(
        Submit.match(check_page.questions[1], str(payoff[0])), 
        str(payoff[0]), p_exec=.8
    )
    check_page.questions[2].submit_functions.clear()
    Debug.send_keys(
        Submit.match(check_page.questions[2], str(payoff[1])),
        str(payoff[1]), p_exec=.8
    )

...
```

### Proposals and responses

It's unlikely the debugger will enter an integer between 0 and the size of the pot, so we'll give our debugger some help:

```python
...

def gen_proposal_input(round_):
    return Debug.send_keys(
        Submit.data_type(
            # REST OF THE FUNCTION HERE
        ),
        str(randint(0, POT)), p_exec=.8
    )

...
```

```python
...

def gen_response_input(round_):
    return Debug.send_keys(
        Submit.data_type(
            # REST OF THE FUNCTION HERE
        ),
        str(randint(0, POT)), p_exec=.8
    )

...
```

## Running the debugger

Now that our debugger won't get stuck in any infinite loops, it's time to run it.

Open two terminal windows. In one, run the hemlock app as usual. In the other, you can run the debugger with hemlock-CLI as follows:

```bash
$ hlk debug
```

To run several AI participants through the survey, e.g. 3, use:

```bash
$ hlk debug -b 3
```

If you don't want to use hemlock-CLI, you can run the debugger with the python interpreter:

```bash
$ python3
>>> from hemlock.debug import AIParticipant, debug
>>> debug() # or debug(<x>) to run x AI participants
```

## Summary

In this part of the tutorial, you learned how to debug your app with hemlock's custom debugging tool.

In the next part of the tutorial, you'll learn how to deploy your application (i.e. put it on the web).
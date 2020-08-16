# Debugging

In the previous part of the tutorial, you implemented the responder branch.

By the end of this part of the tutorial, you'll be able to use hemlock's debugging tool to make sure your app is running smoothly.

Click here to see what your <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.11/blackboard.ipynb" target="_blank">`blackboard.ipynb`</a> and <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.11/survey.py" target="_blank">`survey.py`</a> files should look like at the end of this part of the tutorial.

## Why a custom debugging tool?

In the early days of hemlock, I coded a study in which I asked participants to estimate the ages of people in photographs. I used a submit function to change their data from strings to integers. Everything was running smoothly until one mischievous participant entered 'twenty-seven', breaking my survey and sending me home in a fit of rage.

Since then, I've rewritten my submit functions to be more fault tolerant. If you run

```python
from hemlock import Input, Submit as S

Input(data='twenty-seven', submit=S.data_type(int))._submit().data
```

it doesn't break; it simply converts the data to `None`.

But that wasn't good enough. We often underestimate just how strangely participants will respond to our studies in ways that we can't foresee.

To mitigate this problem, I wrote a custom debugging tool for hemlock. The tool sends an *AI participant* through your survey to check things out. 'AI participant' is a bit of a misnomer; if anything, it's an artificially stupid participant. It clicks random buttons, enters random things into inputs and text boxes, drags range sliders to random values; basically stress testing your code.

## Setup

To run hemlock's custom debugging tool locally, you'll need [Google Chrome](https://www.google.com/chrome/) and [Chromedriver](https://chromedriver.chromium.org/downloads). Check out the setup page for your OS for specific instructions:

- [Windows](../setup/win.md#chromedriver)
- [Windows Subsystem for Linux](../setup/wsl.md#chromedriver)
- [Mac](../setup/mac.md#chromedriver)
- [Linux](../setup/linux.md#chromedriver)

## Basic syntax

Open your jupyter notebook and run the following:

```python
from hemlock import Debug as D, Input

inpt = Input(debug=D.send_keys('hello world'))
inpt.debug
```

Out:

```
[<Debug 1>]
```

You can add debug functions to a page or quesiton by settings its `debug` attribute or passing a `debug` argument to its constructor. Debug functions run when we run the debugger (in just a moment).

As its name suggests, the `send_keys` debug function tells the AI participant to send keys to the input.

Let's watch our debug function at work:

```python
from hemlock import Page
from hemlock.tools import chromedriver

driver = chromedriver()
p = Page(inpt)
p.debug.pop()
p.preview(driver)._debug(driver)
```

First, we use `chromedriver` to open Chromedriver with [selenium python](https://selenium-python.readthedocs.io/).

Next, we create a page with our input question.

We then pop the last debug function from the page we created. Why? By default, pages have two debug functions. The first executes its questions' debug methods in random order; as if the participant were randomly jumping between questions on a page. The second debug function randomly clicks a forward or back button (if it exists), or refreshes the page. Popping the last debug function prevents the debugger from navigating, which allows us to see more clearly what the debugger is doing in preview mode.

Finally, we run the debug function. You'll notice it enters 'hello world' in the input.

After you're done, close the driver:

```python
driver.close()
```

**Notes.**

1. You don't need to run `_debug` yourself in the survey; hemlock takes care of this automatically for you.
2. `send_keys` is just one of many [prebuilt debug functions](../debug_functions.md).

## Default debug functions

We can attach debug functions to pages or questions. Most questions have a default debug function. For example, input questions have a default debug function which sends random ASCII characters to the input. You can see the default debug function at work by running:

```python
p = Page(Input())
p.debug.pop()
p.preview(driver)._debug(driver)
```

However, sometimes we need to attach additional debug functions. For example, our study begins by asking participants to enter their date of birth in `mm/dd/yyyy` format. If you wait for the default debug function to randomly enter a string which matches that pattern, you might not end up running your study before Trump releases his tax returns.

Instead, we'll use something like:

```python
Input(
    '<p>Enter your date of birth.</p>', 
    debug=D.send_keys('10/26/1992')
)
```

Unfortunately, this will not work effectively as a debugger. Sometimes we want the debugger to enter nonsense, and sometimes we want it to enter something sensible. To specify this behavior, we can modify the above:

```python
Input(
    '<p>Enter your date of birth.</p>', 
    debug=[D.send_keys(), D.send_keys('10/26/1992', p_exec=.8)]
)
```

The first debug function, `send_keys()`, sends random keys to the input. The second debug function `send_keys('10/26/1992')`, sends `'10/26/1992'` to the input. We also pass `p_exec=.8` to the second debug function, which specifies its probability of executing. In English, we're telling the debugger, *enter something random, then, with 80% probability, enter something sensible*.

## Custom debug functions

We won't need custom debug functions for our survey, but you may need them elsewhere. Creating custom debug function is similar to creating custom compile, validate, etc. functions, with one important difference: while the functions you've seen take their parent as their first argument, debug functions take a selenium webdriver as their first argument and their parent as their second argument:

```python
@D.register
def f(driver, parent):
    # debug something
```

If you're serious about writing custom debug functions, I recommend checking out the [source code](https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py) for inspiration.

## Debugging our app

First, import `Debug` at the top of `survey.py`:

```python
from hemlock import Branch, Check, Compile as C, Debug as D, Embedded, Input, Label, Navigate as N, Page, Range, Select, Submit as S, Validate as V, route
...
```

Our app can be debugged largely with default debug functions. The exceptions are, 1) the date of birth input, 2) the comprehension check, 3) proposals and responses.

### Date of birth

Modify `survey.py` as follows:

```python
...

@route('/survey')
def start():
    demographics_page = Page(
        Input(
            '<p>Enter your date of birth.</p>',
            ...
            debug=[D.send_keys(), D.send_keys('10/26/1992', p_exec=.8)]
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
    check_page.questions[1].debug = [
        D.send_keys(), D.send_keys(str(payoff[0]), p_exec=.8)
    ]
    check_page.questions[2].debug = [
        D.send_keys(), D.send_keys(str(payoff[1]), p_exec=.8)
    ]

...
```

### Proposals and responses

It's unlikely the debugger will enter an integer between 0 and the size of the pot, so we'll give our debugger some help:

```python
...

def gen_proposal_input(round_):
    return Input(
        ...
        debug=[D.send_keys(), D.send_keys(str(randint(0, POT)), p_exec=.8)]
    )

...
```

```python
...

def gen_response_input(round_):
    return Input(
        ...
        debug=[D.send_keys(), D.send_keys(str(randint(0, POT)), p_exec=.8)]
    )

...
```

## Run the debugger

Now that our debugger won't get stuck in any infinite loops, it's time to run it.

Open another terminal window. As always, change to your project directory:

```bash
$ cd
$ cd my-first-project
```

You should have 3 terminals open: one for jupyter, one for editing `survey.py` and running `hlk serve`, and now a third for running the debugger. In one of the terminal windows, run the hemlock app as usual (`hlk serve`). In the third terminal, run the debugger:

```bash
$ hlk debug
```

To run several AI participants through the survey, e.g. 3, use:

```bash
$ hlk debug -n 3
```

## Summary

In this part of the tutorial, you learned how to debug your app with hemlock's custom debugging tool.

In the next part of the tutorial, you'll learn how to deploy your application (i.e. put it on the web).

<!-- If you don't want to use hemlock-CLI, you can run the debugger with the python interpreter:

```bash
$ python3
>>> from hemlock.debug import AIParticipant, debug
>>> debug() # or debug(3) to run 3 AI participants
``` -->
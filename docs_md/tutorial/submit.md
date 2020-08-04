# Submit

In the previous part of the tutorial, you learned how to validate participant responses.

By the end of this part of the tutorial, you'll be able to run functions to handle form submission.

Click here to see what your <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.4/blackboard.ipynb" target="_blank">`blackboard.ipynb`</a> and <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.4/survey.py" target="_blank">`survey.py`</a> files should look like at the end of this part of the tutorial.

## Why submit functions?

Our demographics page asks participants to enter their date of birth. In addition to date of birth, we also want to record the participant's age.

Submit functions run after a participant submits a page and their responses are validated. We're going to attach a submit function to our date of birth input question to record our participants' age as embedded data.

## Basic syntax

Open your jupyter notebook and run the following:

```python
from hemlock import Input, Submit as S

inpt = Input('<p>Enter "hello world"</p>', submit=S.match('hello world'))
inpt.submit
```

Out:

```
[<Submit 1>]
```

You can add submit functions to a page or question by settings its `submit` attribute or passing a `submit` argument to its constructor. Submit functions run when a participant successfully submits a page.

The `match` submit function changes a question's data to 1 if the data matches a regex pattern, in this case `'hello world'`, and 0 if it does not.

Let's set the input question's data and watch our submit function work:

```python
inpt.data = 'hello world'
inpt._submit().data
```

Out:

```
1
```

```python
inpt.data = 'something other than hello world'
inpt._submit().data
```

Out:

```
0
```

**Notes.**

1. You don't need to run `_submit` yourself in the survey; hemlock takes care of this automatically for you.
2. `match` is just one of many [prebuilt submit functions](../submit_functions.md).

## Custom submission

We're going to use a custom submit function to record our participants' age. Let's see how to do this in our notebook.

```python
from hemlock import Embedded, Page

from datetime import datetime

@S.register
def record_age(inpt):
    # calculate age in years
    date_of_birth = datetime.strptime(inpt.data, '%m/%d/%Y')
    age = (datetime.utcnow() - date_of_birth).days / 365.25
    # record age as embedded data
    inpt.page.embedded = [Embedded('Age', age, data_rows=-1)]

page = Page(
    Input('<p>Enter your date of birth.</p>', submit=S.record_age())
)
inpt = page.questions[0]
inpt.data = '10/26/1992'
inpt._submit()
page.embedded[0].data
```

Out:

```
27.742642026009584
```

### Code explanation

We register a new submit function with the `@S.register` decorator. The submit function takes the input question as its argument. In general, submit functions take their parent as their first argument. `record_age` converts the input's data to a `datetime` object, computes the participant's age, and records it as embedded data.

## Submission in our app

Now that we've seen how to add submit functions in our notebook, let's add it to our app.

In `survey.py`:

```python
from hemlock import Branch, Check, Embedded, Input, Label, Page, Range, Select, Submit as S, Validate as V, route

from datetime import datetime

@route('/survey')
def start():
    return Branch(
        Page(
            Input(
                '<p>Enter your date of birth.</p>',
                placeholder='mm/dd/yyyy',
                var='DoB', data_rows=-1,
                validate=[V.require(), V.date_format()],
                submit=S.record_age()
            ),
            # REST OF THE DEMOGRAPHICS PAGE HERE
        ),
        Page(
            Label('<p>Thank you for completing the survey!</p>'),
            terminal=True
        )
    )

...

@S.register
def record_age(inpt):
    # calculate age in years
    date_of_birth = datetime.strptime(inpt.data, '%m/%d/%Y')
    age = (datetime.utcnow() - date_of_birth).days / 365.25
    # record age as embedded data
    inpt.page.embedded = [Embedded('Age', age, data_rows=-1)]
```

Run the app again, fill in the demographics page, and download the data. You'll now see a variable 'Age' in the data frame.

## Summary

In this part of the tutorial, you learned how create and run submit functions.

In the next part of the tutorial, you'll implement a confirmation page using compile functions.
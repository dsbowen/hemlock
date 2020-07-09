# Submit

In the previous part of the tutorial, you learned how to validate participant responses.

By the end of this part of the tutorial, you'll be able to run functions to handle form submission.

## Why submit functions?

Our demographics page asks participants to enter their date of birth. In addition to date of birth, we also want to record the participant's age.

Submit functions run after a participant submits a page and their responses are validated. We're going to attach a submit function to our date of birth input question to record our participants' age as embedded data.

## Basic syntax

Open your jupyter notebook and run the following:

```python
from hemlock import Input, Submit

inpt = Submit.match(Input('<p>Enter "hello world"</p>'), 'hello world')
inpt
```

Out:

```
<Input 1>
```

`Submit.match` adds a submit function to a question, then returns the question. In this case, the submit function changes its question's data to 1 if the data matches a pattern, `'hello world'`, and 0 if it does not. Submit functions are available in the question's `submit_functions` attribute:

```python
inpt.submit_functions
```

Out:

```
[<Submit 1>]
```

Let's set the input question's reponse and watch our submit function work:

```python
inpt.data = 'hello world'
inpt._submit()
print(inpt.data)

inpt.data = 'something other than hello world'
inpt._submit()
print(inpt.data)
```

Out:

```
1
0
```

`match` is just one of many [prebuilt submit functions](../submit_functions.md).

## Custom submission

We're going to use a custom submit function to record our participants' age.

```python
from hemlock import Embedded, Page

from datetime import datetime

@Submit.register
def record_age(inpt):
    # calculate age in years
    date_of_birth = datetime.strptime(inpt.data, '%m/%d/%Y')
    age = (datetime.utcnow() - date_of_birth).days / 365.25
    # record age as embedded data
    inpt.page.embedded = [Embedded('Age', age, data_rows=-1)]

page = Page(Submit.record_age(Input('<p>Enter your date of birth.</p>')))
inpt = page.questions[0]
inpt.data = '10/26/1992'
inpt._submit()
page.embedded[0].data
```

Out:

```
27.698836413415467
```

### Code explanation

We register a new submit function with the `@Submit.register` decorator. The submit function takes the input question as its argument. It converts the input's data to a `datetime` object, computes the participant's age, and records it as embedded data.

## Submission in our app

Now that we've seen how to add submit functions in our notebook, let's add it to our app.

In `survey.py`:

```python
from hemlock import Branch, Check, Embedded, Input, Label, Page, Range, Select, Submit, Validate, route

from datetime import datetime

@route('/survey')
def start():
    return Branch(
        Page(
            Submit.record_age(Validate.validate_date_format(Input(
                '<p>Enter your date of birth.</p>',
                placeholder='mm/dd/yyyy',
                var='DoB', data_rows=-1
            ))),
            # REST OF THE DEMOGRAPHICS PAGE HERE
        ),
        Page(
            Label('<p>Thank you for completing the survey!</p>'),
            terminal=True
        )
    )

...

@Submit.register
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
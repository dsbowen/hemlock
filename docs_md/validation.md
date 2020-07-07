# Validation

In the previous part of the tutorial, you learned how to create several question polymorphs.

By the end of this part of the tutorial, you'll be able to validate participant responses.

## Basic syntax

Open your jupyter notebook and run the following:

```python
from hemlock import Input, Validate

inpt = Validate.require(Input('<p>You must respond to this question.</p>'))
inpt
```

Out:

```
<Input 1>
```

This code adds validation to an input question. In this case, we require a response from the participant. These validation functions are available in the question's `validate_functions` attribute:

```python
inpt.validate_functions
```

Out:

```
[<Validate 1>]
```

`Validate.require` returns the question it validates, meaning the following code is equivalent:

```python
p = Page(Validate.require(Input('<p>You must respond...</p>')))
```

```python
p = Page(Input('<p>You must respond...</p>'))
Validate.require(p.questions[0]) # questions[0] is the input question
```

We can see that there is currently no response or error associated with the input question:

```python
not inpt.response and not inpt.error
```

Out:

```
True
```

Because the validate function requires a response, and because there is no response, running the validate functions sets the input question's error message as follows:

```python
inpt._validate()
inpt.error
```

Out:

```
Please respond to this question.
```

You don't need to run `_validate()` yourself in the survey; hemlock takes care of this automatically for you.

`require` is just one of many [prebuilt validate functions](validate_functions.md).

## Custom validation

This is a good start, but what happens when someone enters a nonsense response for date of birth?

For this, we're going to need a custom validate function. Let's see how to do this in our notebook.

```python
from datetime import datetime

@Validate.register
def validate_date_format(inpt):
    try:
        # try to convert to a datetime object
        datetime.strptime(inpt.response, '%m/%d/%Y')
    except:
        # if this fails, the participant entered an invalid response
        return '<p>Make sure to format your date of birth as mm/dd/yyyy.</p>'
    
Validate.validate_date_format(inpt)
inpt.response = '''
I, George Thaddeus Thatch the Third, was born in the first fortnight of August 1792.
'''
inpt._validate()
inpt.error
```

Out:

```
Make sure to format your date of birth as mm/dd/yyyy.
```

### Code explanation

First, we import `datetime`, a native python package for handling dates and times. 

Next, we register a new validate function with the `@Validate.register` decorator. The validate function takes the input question as its argument. In general, validate functions (and, as we will see, their cousins compile, submit, and navigate functions) take their 'parent' (usually a branch, page, or question) as their first argument.

The validate function tries to convert the input question's response to a `datetime` object and returns an error message if this fails. In general, validate functions return an error message (a string) if there is a problem, and `None` if the response is valid.

## Validation in the app

Now that we've seen how to add validation in our notebook, let's add it to our app.

In `survey.py`:

```python
from hemlock import Branch, Check, Input, Page, Label, Range, Select, Validate, route

from datetime import datetime

@Validate.register
def validate_date_format(inpt):
    try:
        # try to convert to a datetime object
        datetime.strptime(inpt.response, '%m/%d/%Y')
    except:
        # if this fails, the participant entered an invalid response
        return '<p>Make sure to format your date of birth as mm/dd/yyyy.</p>'

@route('/survey')
def start():
    return Branch(
        Page(
            Validate.validate_date_format(Validate.require(Input(
                '<p>Please enter your date of birth in mm/dd/yyyy format.</p>'
            ))),
            Validate.require(Check(
                '<p>Please indicate your gender.</p>',
                ['Male', 'Female', 'Other']
            )),
            # WRAP THE OTHER QUESTIONS IN Validate.require
            ...
```

Run the app again and try to continue past the demographics page; enter and invalid date of birth, leave some questions blank, and see your validation at work.

**Note.** Validate functions run in order, stopping with the first validate function which returns an error. So `Validate.validate_date_format(Validate.require(Input('...')))` first runs `require` then, if the participant responded, runs `validate_date_format`.

## Summary

In this part of the tutorial, you learned how to validate participant responses.

In the next part of the tutorial, you'll learn how to run submit functions and create embedded data.
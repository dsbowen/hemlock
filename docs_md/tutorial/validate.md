# Validation

In the previous part of the tutorial, you learned how to store and download data.

By the end of this part of the tutorial, you'll be able to validate participant responses.

Click here to see what your <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.3/blackboard.ipynb" target="_blank">`blackboard.ipynb`</a> and <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.3/survey.py" target="_blank">`survey.py`</a> files should look like at the end of this part of the tutorial.

## Why validation?

I often run studies where I elicit numerical estimates. Early on, I noticed that a small but annoying faction of participants, rather than entering actual numbers (e.g. 50), answered the question in full sentences:

> I believe the answer is fifty.

We often need to make sure participants are entering the right kind of answer, whether it's typing the same password twice, answering a comprehension check by clicking on the correct choice, or entering a number instead of a word.

## Basic syntax

Open your jupyter notebook and run the following:

```python
from hemlock import Input, Validate as V

inpt = Input(validate=V.require())
inpt.validate
```

Out:

```
[<Validate 1>]
```

You can add validate functions to a page or question by setting its `validate` attribute or passing a `validate` argument to its constructor. Validate functions run when a participant attempts to submit a page. If the participant's response is valid, the function returns `None`, allowing the participant to continue the survey. If the participant's response is invalid, the function returns an error message.

As its name indicates, the validate function requires the participant to respond to the input question. By default, the input question has no response. It also has no error message. We can see this as follows:

```python
(
    'The input has no response or error message', 
    not inpt.response and not inpt.error
)
```

Out:

```
('The input has no response or error message', True)
```

Now, let's run the validate function. Because the input question has no response, the validate function will return an error message. This error message is stored in the input question's `error` attribute:

```python
inpt._validate()
inpt.error
```

Out:

```
'Please respond to this question.'
```

**Notes:**

1. You don't need to run `_validate` yourself in the survey; hemlock takes care of this automatically for you.
2. `require` is just one of many [prebuilt validate functions](../validate_functions.md).

## Custom validation

This is a good start, but what happens when someone enters a nonsense response for date of birth?

For this, we're going to need a custom validate function. Let's see how to do this in our notebook:

```python
from datetime import datetime

@V.register
def date_format(inpt):
    try:
        # try to convert to a datetime object
        datetime.strptime(inpt.response, '%m/%d/%Y')
    except:
        # if this fails, the participant entered an invalid response
        return '<p>Format your date of birth as mm/dd/yyyy.</p>'
    
inpt = Input(validate=V.date_format())
inpt.response = '''
I, George Thaddeus Thatch the Third, was born in the first fortnight of August 1792.
'''
inpt._validate()
inpt.error
```

Out:

```
Format your date of birth as mm/dd/yyyy.
```

## Code explanation

First, we import `datetime`, a native python package for handling dates and times.

Next, we register a new validate function with the `@V.register` decorator. The validate function tries to convert the input question's response to a `datetime` object and returns an error message if this fails.

It's worth re-emphasizing that `V.my_function` does *not* return the result of `my_function`. `V.my_function` returns `<Validate x>`, which will call `my_function` later, when the participant attempts to submit the page.

Note that `date_format` takes an input question as its argument. In general, validate functions take their 'parent' (the branch, page, or question to which they belong) as their first argument. The arguments passed to `V.my_function` will be passed to `my_function` *after* the parent. For example:

```python
@V.register
def my_function(parent, my_argument):
    print('My parent is:', parent)
    print('My argument is:', my_argument)
    
inpt = Input(validate=V.my_function('hello world'))
inpt
```

Out:

```
<Input 1>
```

In:

```python
inpt._validate()
```

Out:

```
My parent is: <Input 1>
My argument is: hello world
```

The same pattern holds for the other function models (submit, compile, and navigate functions) we will see in the coming sections.

## Validation in our app

Now that we've seen how to add validation in our notebook, let's add it to our app.

In `survey.py`:

```python
from hemlock import Branch, Check, Input, Label, Page, Range, Select, Validate as V, route

from datetime import datetime

@route('/survey')
def start():
    return Branch(
        Page(
            Input(
                '<p>Enter your date of birth.</p>',
                placeholder='mm/dd/yyyy',
                var='DoB', data_rows=-1, 
                validate=V.date_format()
            ),
            Check(
                '<p>Indicate your gender.</p>',
                ['Male', 'Female', 'Other'],
                var='Gender', data_rows=-1,
                validate=V.require()
            ),
            # REST OF THE DEMOGRAPHICS PAGE HERE
        ),
        Page(
            Label('<p>Thank you for completing the survey!</p>'), 
            terminal=True
        )
    )

@V.register
def date_format(inpt):
    try:
        # try to convert to a datetime object
        datetime.strptime(inpt.response, '%m/%d/%Y')
    except:
        # if this fails, the participant entered an invalid response
        return '<p>Format your date of birth as mm/dd/yyyy.</p>'
```

Run the app again and try to continue past the demographics page; enter an invalid date of birth, leave some questions blank, and see your validation at work.

## Multiple validate functions

You can attach multiple validation functions by setting `validate` to a list of functions. Validate functions run in the order in which you add them, stopping with the first validate function which returns an error. Try adding `require` to the date of birth question by changing `validate=V.date_format()` to `validate=[V.require(), V.date_format()]`.

Run your app and leave the date of birth empty. The error message will be, `'Please respond to this question.'`. Enter an invalid date of birth. The error message will be `'Format your date of birth as mm/dd/yyyy.'`.

## Summary

In this part of the tutorial, you learned how to validate participant responses.

In the next part of the tutorial, you'll learn how to run submit functions to modify participant data after they submit a page.
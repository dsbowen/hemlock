# Compile

In the previous part of the tutorial, you learned how to run functions to handle form submission.

In this part of the tutorial, you'll implement a confirmation page using compile functions.

## Why compile functions?

Compile functions run just before a page's html is compiled. This allows us to make our survey responsive to participants.

In our case, we're going to make a confirmation page for the participant's demographic information.

## Basic syntax

Open your jupyter notebook and run the following:

```python
from hemlock import Check, Compile

check = Compile.shuffle(Check(
    '<p>Select the correct answer.</p>',
    ['correct', 'incorrect', 'also incorrect']
))
check._compile()
[choice.label for choice in check.choices]
```

Out:

```
['also incorrect', 'incorrect', 'correct']
```

Run this a few times and notice how the order of the choices changes. This particular behavior is useful for comprehension checks, as we'll see later.

`Compile.shuffle` adds a compile function to a page or question, then returns the page or question. In this case, we shuffle the choices of a check question every time the participant reloads the page. Compile functions are available in the question's `compile_functions` attribute:

```python
check.compile_functions
```

Out:

```
[<Compile 1>]
```

## Custom compilation

We want to take the participant's responses to the demographics page and display them on a new page. We'll ask the participant to correct any errors by going back to the demographics page.

Let's see how to do this in our notebook:

```python
from hemlock import Input, Label, Page
from hemlock.tools import join

@Compile.register
def confirm(label, demographics_page):
    # get the participant's data from the demographics page
    demographics = [q.data for q in demographics_page.questions]
    # re-format the race demographic data
    race = demographics_page.questions[2]
    race = join('and', *(key for key in race.data if race.data[key]))
    demographics[2] = race
    # set the label based on the participant's demographics data
    label.label = '''
    <p>Confirm the following information:</p>
    <ul>
        <li>Date of birth: {}</li>
        <li>Gender: {}</li>
        <li>Race/Ethnicity: {}</li>
        <li>Marital status: {}</li>
        <li>Subjective socio-economic status: {}</li>
    </ul>
    <p>To correct this information, click '<<'.</p>
    '''.format(*demographics)
    
demographics_page = Page(
    Input(data='10/26/1992'),
    Check(data='Male'),
    Check(data={'White': 1, 'Black': 1}),
    Select(data='Never married'),
    Range(data='5')
)
p = Page(Compile.confirm(Label(), demographics_page), back=True)
p._compile().preview()
```

### Code explanation

First, we register a new compile function with the `@Compile.register` decorator. The compile function takes a page or question as its argument. We also pass in the demographics page as the compile function's second argument.

Next, we add a back button to the page with `back=True`.

Then, we compile and preview the page. Note that you won't need to run `_compile` in your survey files; hemlock does this automatically for you.

Our `confirm` function begins by gathering the demographics data from the demographics page. The data are well formatted to insert into our confirmation page except for race. For `Check` and `Select` questions, if the participant can select multiple choices, the data are stored as a dictionary mapping choice values (`'White'`, `'Black'`, etc.) to a 0-1 indicator that the participant selected that choice. We fix this with the following:

```python
from hemlock.tools import join

race_data = demographics_page.questions[2].data
race = join('and', *(key for key in race_data if race_data[key]))
demographics[2] = race
```

Note that `race_data[key]` evaluates to `True` if the `key` (`'White'`, `'Black'`, etc.) was selected. So the expression `(key for key in race_data if race_data[key])` means 'get all the keys (races) the participant selected'. The expression

```python
join('and', *(key for key in race_data if race_data[key]))
```

means 'join all of the selected keys with "and", e.g. "White and Black"'.

Finally, our compile function adds the demographics to the confirmation page.

## Compilation in our app

Now that we've seen how to add compile functions in our notebook, let's add it to our app.

In `survey.py`:

```python
from hemlock import Branch, Check, Compile, Embedded, Input, Label, Page, Range, Select, Submit, Validate, route
from hemlock.tools import join

from datetime import datetime

@route('/survey')
def start():
    demographics_page = Page(
        Submit.record_age(Validate.validate_date_format(Input(
            '<p>Enter your date of birth.</p>',
            placeholder='mm/dd/yyyy',
            var='DoB', data_rows=-1
        ))),
        # REST OF THE DEMOGRAPHICS PAGE HERE
    )
    return Branch(
        demographics_page,
        Page(
            Compile.confirm(Label(), demographics_page), 
            back=True, 
            terminal=True
        )
    )

...

@Compile.register
def confirm(label, demographics_page):
    # PUT YOUR COMPILE FUNCTION HERE
```

Run the app again to see your confirmation page.

## Summary

In this part of the tutorial, you implemented a confirmation page using compile functions.

In the next part of the tutorial, you'll learn how to set up navigation between branches.
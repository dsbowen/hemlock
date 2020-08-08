# Question polymorphs

In the previous part of the tutorial, you learned how to initialize a hemlock application and run it locally.

By the end of this part of the tutorial, you'll be able to add a variety of question polymorphs to your survey pages.

Click here to see what your <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.1/blackboard.ipynb" target="_blank">`blackboard.ipynb`</a> and <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.1/survey.py" target="_blank">`survey.py`</a> files should look like at the end of this part of the tutorial.

## Creating a demographics page

We'll use jupyter notebook as a blackboard to iterate on our demographics page design. After pushing the application context, we'll create the following page:

```python
from hemlock import Check, Input, Page, Label, Range, Select

p = Page(
    Input(
        '<p>Enter your date of birth.</p>',
        placeholder='mm/dd/yyyy'
    ),
    Check(
        '<p>Indicate your gender.</p>',
        ['Male', 'Female', 'Other']
    ),
    Check(
        '<p>Indicate your race or ethnicity. Check as many as apply.</p>',
        [
            'White',
            'Black or African-American',
            'Asian',
            'Native Hawaiian or other Pacific Islander',
            'Other',
        ],
        multiple=True
    ),
    Select(
        '<p>Select your current marital status.</p>',
        [
            'Married',
            'Widowed',
            'Divorced',
            'Separated',
            'Never married',
        ]
    ),
    Range(
        '''
        <p>At the right end of the scale are the people who are the 
        best off; those who have the most money, the most 
        education, and the best jobs. On the left are the people 
        who are the worst off; those who have the least money, the 
        least education, and the worst jobs (or are unemployed). 
        Please indicate where you think you stand on this scale.</p>
        ''',
        min=0, max=10
    ),
)
```

As usual, use `p.preview()` to preview the page and `[os.remove(f) for f in app.tmpfiles if os.path.exists(f)]` when you're done.

## Code explanation

Here we add several 'question polymorphs' (i.e. types of questions) to our page. 

The first is an input. We add `placeholder='mm/dd/yyyy'`, telling participants the expected format of their date of birth.

The next two are check questions, which allow participants to check one or more choices. Notice that the first check question allows participants to check only one choice; we allow participants to check multiple choices in the second check question by passing `multiple=True`.

The fourth question is a select (dropdown) question. If we wanted, we also could have passed `multiple=True` to its contructor to allow participants to select multiple options.

Our final question is a range slider. By default, it goes from 0 to 100, but we set its range from 0 to 10 here.

## Adding the page to the survey

Once we're satisfied with the preview, we incorporate the page into our survey. Our `survey.py` file should be:

```python
from hemlock import Branch, Check, Input, Page, Label, Range, Select, route

@route('/survey')
def start():
    return Branch(
        Page(
            Input(
                '<p>Enter your date of birth.</p>',
                placeholder='mm/dd/yyyy'
            ),
            # INSERT THE REST OF THE DEMOGRAPHICS PAGE HERE
        ),
        Page(
            Label('<p>Thank you for completing this survey.</p>'), 
            terminal=True
        )
    )
```

## Summary

In this part of the tutorial, you learned how to create a demographics questionnaire using several question polymorphs.

In the next part of the tutorial, you'll learn how to store and download survey data.
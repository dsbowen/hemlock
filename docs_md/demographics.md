# Demographics

In the previous part of the tutorial, you learned how to initialize a hemlock application and run it locally.

By the end of this part of the tutorial, you'll be able to add a variety of questions to your survey pages to create a demographics questionnaire.

## Creating the demographics page

We'll use jupyter notebook as a blackboard to iterate on our demographics page design.

After pushing the application context, we'll create a page with an input question and ask participants to enter their age.

```python
from hemlock import Check, Input, Page, Label, Range, Select

p = Page(
    Input('<p>Please enter your date of birth in mm/dd/yyyy format.</p>'),
    Check(
        '<p>Please indicate your gender.</p>',
        ['Male', 'Female', 'Other']
    ),
    Check(
        '<p>Please indicate your ethnicity. Check as many as apply.</p>',
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
        '<p>Please select your current marital status.</p>',
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

As usual, enter `p.preview()` (or `p.preview('Ubuntu')`) preview the page.

### Code explanation

Here we add several 'question polymorphs' (i.e. types of questions) to our page. 

The first is a free form input. 

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
                '<p>Please enter your date of birth in mm/dd/yyyy format.</p>'
            ),
            Check(
                '<p>Please indicate your gender.</p>',
                ['Male', 'Female', 'Other']
            ),
            Check(
                '<p>Please indicate your ethnicity. Check as many as apply.</p>',
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
                '<p>Please select your current marital status.</p>',
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
        ),
        Page(
            Label('<p>Thank you for completing this survey.</p>'), 
            terminal=True
        )
    )
```

## Summary

In this part of the tutorial, you learned how to create a demographics questionnaire using several question polymorphs.

In the next part of the tutorial, you'll learn how to validate participant responses.
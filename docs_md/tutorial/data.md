# Data

In the previous part of the tutorial, you learned how to create a demographics questionnaire using several question polymorphs.

By the end of this part of the tutorial, you'll be able to store and download data.

Click here to see what your <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.2/blackboard.ipynb" target="_blank">`blackboard.ipynb`</a> and <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.2/survey.py" target="_blank">`survey.py`</a> files should look like at the end of this part of the tutorial.

## Previewing data from a single participant

Each hemlock project has a downloadable data frame containing the data for all participants. We'll start by looking at the data belonging to a 'test participant'.

Run the following in your jupyter notebook:

```python
from hemlock import Participant

part = Participant.gen_test_participant()
dict(part.get_data())
```

Out:

```
{'ID': [1],
 'EndTime': [datetime.datetime(2020, 7, 8, 11, 46, 54, 462552)],
 'StartTime': [datetime.datetime(2020, 7, 8, 11, 46, 54, 462552)],
 'Status': ['InProgress']}
```

This shows the data our test participant contributes to the data frame. The keys are variable names, and values are list of entries for that variable.

An easy way to add data is with 'embedded data':

```python
from hemlock import Embedded

part.embedded = [Embedded(var='MyVariable', data='MyData')]
dict(part.get_data())
```

Out:

```
{'ID': [1],
 'EndTime': [datetime.datetime(2020, 7, 8, 11, 46, 54, 462552)],
 'StartTime': [datetime.datetime(2020, 7, 8, 11, 46, 54, 462552)],
 'Status': ['InProgress'],
 'MyVariable': ['MyData'],
 'MyVariableOrder': [0],
 'MyVariableIndex': [0]}
```

This adds an `Embedded` data object to our participant. Embedded data are a type of data element, like questions, but unlike questions, are not displayed to participants. We can add embedded data to a participant, branch, or page.

When we examine the data, we see that the participant has a new variable named `'MyVariable'` with data `['MyData']`. We also see two additional variables named `'MyVariableOrder'` and `'MyVariableIndex'`. Hemlock automatically adds order and index data for every data element. Order is the order in which this data element appeared in the survey, relative to other data elements belonging to the same variable. Index is the order in which this data element appeared in its parent's list of children; for example, the order in which a question appeared on its page.

## Ordering

The order in which data elements appear in the data frame is the order in which they were created; not necessarily the order in which they appear to the participant. For example:

```python
embedded1 = Embedded('MyVariable', 1)
embedded0 = Embedded('MyVariable', 0)
part.embedded = [embedded0, embedded1]
dict(part.get_data())
```

Out:

```
{'ID': [1, 1],
 'EndTime': [datetime.datetime(2020, 7, 8, 11, 46, 54, 462552),
  datetime.datetime(2020, 7, 8, 11, 46, 54, 462552)],
 'StartTime': [datetime.datetime(2020, 7, 8, 11, 46, 54, 462552),
  datetime.datetime(2020, 7, 8, 11, 46, 54, 462552)],
 'Status': ['InProgress', 'InProgress'],
 'MyVariable': [1, 0],
 'MyVariableOrder': [1, 0],
 'MyVariableIndex': [1, 0]}
```

Note that the data for `'MyVariable'` are `[1, 0]` because we created `embedded1` before `embedded0`.

## Data rows

By default, data elements (embedded data and questions) contribute 1 row to the data frame. But we often want the same data to be repeated on multiple rows. We do this by setting the `data_rows` attribute:

```python
part.embedded = [Embedded('MyVariable', 'MyData', data_rows=3)]
dict(part.get_data())
```

Out:

```
{'ID': [1, 1, 1],
 'EndTime': [datetime.datetime(2020, 7, 8, 11, 46, 54, 462552),
  datetime.datetime(2020, 7, 8, 11, 46, 54, 462552),
  datetime.datetime(2020, 7, 8, 11, 46, 54, 462552)],
 'StartTime': [datetime.datetime(2020, 7, 8, 11, 46, 54, 462552),
  datetime.datetime(2020, 7, 8, 11, 46, 54, 462552),
  datetime.datetime(2020, 7, 8, 11, 46, 54, 462552)],
 'Status': ['InProgress', 'InProgress', 'InProgress'],
 'MyVariable': ['MyData', 'MyData', 'MyData'],
 'MyVariableOrder': [0, 0, 0],
 'MyVariableIndex': [0, 0, 0]}
```

Additionally, we often want to 'fill in' rows of a variable to match the length of a data frame. For example, we may not know in advance how many rows a participant will contribute to the data frame, but we know that we want the participant's demographic information to appear on all rows. To do this, we set `data_rows` to a negative number. For example, `data_rows=-2` means 'fill in two rows with this data entry and, when you download the data, fill in any blank rows after this with the same data':

```python
part.embedded = [
    # these data will fill in empty rows at the bottom of the data frame
    Embedded('MyFilledVariable', 'MyFilledData', data_rows=-1),
    # these data will appear on three rows of the data frame
    Embedded('MyVariable', 'MyData', data_rows=3)
]
dict(part.get_data())['MyFilledVariable']
```

Out:

```
['MyFilledData', 'MyFilledData', 'MyFilledData']
```

## Adding data to our survey

We can add data to our existing survey in much the same way: by setting a question's `var` and (when necessary) `data_rows` attribute. We generally want demographics information to appear in all rows of the data frame, so we'll set `data_rows=-1`.

In `survey.py`:


```python
...

@route('/survey')
def start():
    return Branch(
        Page(
            Input(
                '<p>Enter your date of birth.</p>',
                placeholder='mm/dd/yyyy',
                var='DoB', data_rows=-1
            ),
            Check(
                '<p>Indicate your gender.</p>',
                ['Male', 'Female', 'Other'],
                var='Gender', data_rows=-1
            ),
            # SET THE `var` AND `data_rows` ATTRIBUTES FOR THE REST OF THE QUESTIONS
            ...
```

**Note.** When a participant submits a page, the questions' data are recorded in a `data` attribute. A question's data will be added to the data frame if and only if you set its `var` attribute. However, data will be stored in a question's `data` attribute whether or not the `var` attribute is set.

## Downloading data

Run your survey locally, fill in the demographics page, and continue to the end of the survey. Your data will be recorded in the database.

To download your data, navigate to <http://localhost:5000/download> in your browser. Select 'Data frame', then click the download button. This will download a zip file containing your data in .csv format. 

Take a look at the data. In addition to what we've already covered, there are a few things to notice:

1. Variables like `GenderMaleIndex` and `GenderFemaleIndex` record the order in which a question displayed its choices.
2. The data of questions for which you can select multiple choices are automatically one-hot encoded. For example, if `RaceWhite` and `RaceAsian` are both 1, and the rest of the race variables are 0, this means means the participant is part White and part Asian.

## Summary

In this part of the tutorial, you learned how to store and download data.

In the next part of the tutorial, you'll implement validation for participant responses.
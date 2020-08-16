# Navigate

In the previous part of the tutorial, you implemented a confirmation page using compile functions.

By the end of this part of the tutorial, you'll be able to set up navigation between branches.

Click here to see what your <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.6/blackboard.ipynb" target="_blank">`blackboard.ipynb`</a> and <a href="https://github.com/dsbowen/hemlock-tutorial/blob/v0.6/survey.py" target="_blank">`survey.py`</a> files should look like at the end of this part of the tutorial.

## Why navigate functions?

Navigate functions move participants through different branches of the survey. For example, participants in the control group might follow one branch, while participants in the treatment group follow another.

In our case, we'll use a navigate function to bring participants from the demographics branch of our survey to an 'utlimatum game' branch. In this branch, participants will play an ultimatum game with each other.

## Basic syntax

Open your jupter notebook and run the following:

```python
from hemlock import Branch, Navigate as N, Page, Participant

def start():
    return Branch(
        Page(), 
        Page(), 
        navigate=N.end()
    )

@N.register
def end(start_branch):
    return Branch(Page(terminal=True))

part = Participant.gen_test_participant(start)
part.view_nav()
```

Out:

```
 <Branch 1>
 <Page 1> C 
 <Page 2>  

 C = current page 
 T = terminal page
```

You can add navigate functions to a branch or page by setting its `navigate` attribute or passing a `navigate` argument to its constructor. Navigate functions bring participants to a new branch when they have completed the branch or page to which the navigate function belongs.

### Code explanation

Unlike validate, submit, and compile functions, there are no prebuilt navigate functions. We register a custom navigate function with the `@N.register` decorator. The navigate function takes the start branch (the branch returned by `start`) as its first argument. In general, navigate functions take an 'origin' branch or page as their first argument. Navigate functions return a `Branch` object.

`part.view_nav()` prints the participant's 'branch stack'. Right now the participant is on the branch created by `start`. Let's make our test participant navigate forward and view the navigation again:

```python
part.forward().view_nav()
```

Out:

```
 <Branch 1>
 <Page 1>  
 <Page 2> C 

 C = current page 
 T = terminal page
```

And again:

```python
part.forward().view_nav()
```

Out:

```
 <Branch 1>
 <Page 1>  
 <Page 2>  
     <Branch 2>
     <Page 3> C T
```

What happened? Our participant reached the end of the `start` branch (branch 1) and navigated to the `end` branch (branch 2). It's currently on page 3, which is the last (terminal) page of the survey.

**Note.** You won't call `view_nav` or `forward` in the survey; hemlock takes care of the navigation automtically for you. These are just useful for debugging in jupyter.

## Branching off pages

Branching off of branches allows us to navigate to a new branch at the end of our current branch. But occasionally, we'll want to navigate to a new branch from the middle of our current branch. To do this, we'll branch off of a page.

This time, instead of attaching the navigate function to the branch, we'll attach it to the first page of the branch:

```python
def start():
    return Branch(Page(navigate=N.middle()), Page(terminal=True))

@N.register
def middle(start_branch):
    return Branch(Page())

part = Participant.gen_test_participant(start)
```

As before, run `part.view_nav()` and `part.forward()` a few times. This is what you'll see:

```
 <Branch 1>
 <Page 1> C 
 <Page 2> T
```

```
 <Branch 1>
 <Page 1> 
     <Branch 2>
     <Page 3> C 
 <Page 2> T
```

```
 <Branch 1>
 <Page 1> 
     <Branch 2>
     <Page 3> 
 <Page 2> C T
```

What happened? We started on the first page of the `start` branch (branch 1, page 1). Then, we branched off of page 1 to the `middle` branch (branch 2, page 3). At the end of the `middle` branch, we picked up where we left off on the `start` branch (branch 1, page 2).

## Navigating back

You'll often want to allow participants to navigate to a previous page. To do this, simply set a page's `back` attribute to `True`, or pass `back=True` to a page's constructor. 

You can also navigate backward in the notebook. Run this line a few times:

```python
part.back().view_nav()
```

Out:

```
 <Branch 1>
 <Page 1> 
     <Branch 2>
     <Page 3> C 
 <Page 2> T

 C = current page 
 T = terminal page
```

```
 <Branch 1>
 <Page 1> C 
 <Page 2> T

 C = current page 
 T = terminal page
```

## Navigation in our app

Now that we've seen how to add navigate functions in our notebook, let's add it to our app.

In `survey.py`:

```python
from hemlock import Branch, Check, Compile as C, Embedded, Input, Label, Navigate as N, Page, Range, Select, Submit as S, Validate as V, route

...

@route('/survey')
def start():
    ...
    return Branch(
        demographics_page,
        Page(
            Label(compile=C.confirm(demographics_page)),
            back=True # DELETE terminal=True
        ),
        navigate=N.ultimatum_game()
    )

...

@N.register
def ultimatum_game(start_branch):
    return Branch(
        Page(
            Label('<p>You are about to play an ultimatum game...</p>'),
            terminal=True
        )
    )
```

Run the app again and navigate past the demographics page. You'll find yourself on our new ultimatum game branch.

## Summary

In this part of the tutorial, you learned how to navigate between branches. 

In the next part of the tutorial, we'll tie together some of the things you've learned about page logic.
# Navigate

In the previous part of the tutorial, you implemented a confirmation page using compile functions.

By the end of this part of the tutorial, you'll be able to set up navigation between branches.

## Why navigate functions?

Navigate functions move participants through different branches of the survey. For example, participants in the control group might follow one branch, while participants in the treatment group follow another.

In our case, we'll use a navigate function to bring participants from the demographics branch of our survey to a branch in which participants will an ultimatum game with each other.

## Basic syntax

Open your jupter notebook and run the following:

```python
from hemlock import Branch, Navigate, Page, Participant

def start():
    return Navigate.end(Branch(Page(), Page()))

@Navigate.register
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

Unlike validate, submit, and compile functions, there are no prebuilt navigate functions. We register a custom navigate function with the `@Navigate.register` decorator. The navigate function takes an 'origin' branch or page as its first argument (in this case, the branch returned by `start`). Navigate functions return a `Branch` object.

After registering `end` as a navigate function, `Navigate.end` adds the navigate function to a branch or page, then returns the branch or page to which it was added. Once the participant reaches the end of the branch returned by `start`, they are brought to the branch returned by `end`.

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

**Note.** You won't call `view_nav` or `forward` in the survey; hemlock takes care of the navigation for you. These are just useful for debugging in jupyter.

## Branching off pages

Branching off of branches allows us to navigate to a new branch at the end of our current branch. But occasionally, we'll want to navigate to a new branch from the middle of our current branch. To do this, we'll branch off of a page.

This time, instead of attaching the navigate function to the branch, we'll attach it to the first page of the branch:

```python
from hemlock import Branch, Navigate, Page, Participant

def start():
    return Branch(Navigate.middle(Page()), Page(terminal=True))

@Navigate.register
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

**Note.** Going back is just as easy. Simply use `my_page.back=True`. To play with this in the notebook, use `my_participant.back()` instead of `my_participant.forward()`.

## Navigation in our app

Now that we've seen how to add navigate functions in our notebook, let's add it to our app.

In `survey.py`:

```python
from hemlock import Branch, Check, Compile, Embedded, Input, Label, Navigate, Page, Range, Select, Submit, Validate, route
from hemlock.tools import join

from datetime import datetime

@route('/survey')
def start():
    demographics_page = Page(
        # DEMOGRAPHICS PAGE HERE
    )
    return Navigate.ultimatum_game(Branch(
        demographics_page,
        Page(Compile.confirm(Label(), demographics_page), back=True)
    ))

...

@Navigate.register
def ultimatum_game(start_branch):
    return Branch(Page(
        Label('<p>You are about to play an ultimatum game...</p>'), 
        terminal=True
    ))
```

Run the app again and navigate past the demographics page. You'll find yourself on our new ultimatum game branch.

## Summary

In this part of the tutorial, you learned how to navigate between branches. 

In the next part of the tutorial, we'll tie together some of the things you've learned about page logic.
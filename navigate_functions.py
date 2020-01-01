"""Navigate functions"""

import tools

from hemlock import *

@Navigate.register
def NavigateFunctions(origin=None):
    b = Branch()
    Navigate.NewBranch0(b)
    return b

@Navigate.register
def NewBranch0(origin=None):
    b = Branch()
    Navigate.NewBranch1(b)

    p = Page(b, back=False)
    Label(
        p, 
        label="<p>Turn the forward and back buttons on and off by setting a `Page`'s `forward` and `back` attributes to `True` and `False`.</p>"
    )
    select_forward_btn = Check(
        p,
        label='<p>Do you want the forward button to appear on the next page?</p>',
    )
    Choice(select_forward_btn, label='Yes', value=1)
    Choice(select_forward_btn, label='No', value=0)

    p = Page(b)
    Compile.set_forward_btn(p, select_forward_btn)
    Label(p)

    return b

@Compile.register
def set_forward_btn(page, select_forward_btn):
    page.forward = bool(select_forward_btn.data)
    if select_forward_btn.data:
        page.questions[0].label = '<p>Behold! The forward button has appeared.</p>'
    else:
        page.questions[0].label = '<p>Behold! The forward button has disappeared.</p>'

@Navigate.register
def NewBranch1(origin=None):
    b = Branch()
    Navigate.NewBranch3(b)

    p = Page(b)
    Navigate.NewBranch2(p)
    Label(
        p,
        label='<p>You can also attach `Navigate` functions to `Page`s.</p>'
    )

    return b

@Navigate.register
def NewBranch2(origin=None):
    b = Branch()
    p = Page(b)
    Label(
        p,
        label='<p>This `Branch` was created by `NewBranch2`, and originated from {}.</p>'.format(origin.model_id)
    )
    return b

@Navigate.register
def NewBranch3(origin=None):
    b = Branch()
    Navigate.NewBranch4(b)

    p = Page(b)
    Label(
        p,
        label='<p>This `Branch` was created by `NewBranch3`, and originated from {}.</p>'.format(origin.model_id)
    )

    p0 = Page(b)
    Label(
        p0,
        label="""
        <p>You are about to embark on a journey using the `forward_to` and `back_to` attributes to skip over pages.</p>
        <p>You begin your journey on page 0.</p>
        """
    )

    p1 = Page(b, back=False)
    Label(
        p1, 
        label="""
        <p>You now find yourself on page 1.</p>
        <p>But if you cannot go forward from page 2, how will can you complete your journey?</p>
        """
    )

    p2 = Page(b, forward=False)
    Label(
        p2, 
        label="""
        <p>It appears you have skipped over page 1 and find yourself trapped on page 2!</p>
        <p>But sometimes, only by going back can we hope to move forward.</p>
        """
    )
    p0.forward_to = p2

    p3 = Page(b, back_to=p0)
    Label(
        p3,
        label="""
        <p>Welcome to page 3, and congratulations on escaping page 2!</p>
        <p>Click forward to continue, or back to restart your journey.</p>
        """
    )
    p1.forward_to = p3

    return b

@Navigate.register
def NewBranch4(origin=None):
    b = Branch()
    Navigate.NewBranch5(b)
    p = Page(b)
    Input(
        p,
        label="""
        <p>This is branch {}.</p>
        <p>The `Navigation` function which created it creates a new `Branch` every time it runs.</p>
        <p>From the participant's perspective, all inputs on this branch will be cleared.</p>
        <p>Go back and forth the see that a new branch is created and this input appears to be cleared.<p>
        """.format(b.id)
    )
    return b

@Navigate.register
def NewBranch5(origin=None):
    if origin.next_branch is not None:
        return origin.next_branch
    b = Branch()
    Navigate.Tools(b)
    p = Page(b)
    Input(
        p,
        label="""
        <p>This is branch {}.</p>
        <p>You can reuse the original `Branch` created by this `Navigate` function with the `origin`'s `next_branch` attribute.</p>
        <p>Go back and forth to see that this is the same branch each time and that the input is saved.</p>
        """.format(b.id)
    )
    return b
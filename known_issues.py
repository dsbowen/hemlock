from hemlock import Branch, Compile, Label, Page, route
from hemlock.tools import comprehension_check

# @route('/survey')
# def start():
#     page0 = Page(Label('0'))
#     page1 = Page(Label('1'))
#     page2 = Page(Label('2'))
#     branch = Branch(page0, page1, page2, Page(terminal=True))
#     # branch = Branch(page1, page2, Page(terminal=True))
#     Compile.f(page1, page0=page0)
#     Compile.f(page2, page0=page0)
#     # branch.pages.insert(0, page0)
#     return branch

@route('/survey')
def start():
    page0 = Page(Label('0'))
    lab = page0.questions[0]
    page1 = Page(Label('1'))
    page2 = Page(Label('2'))
    # branch = Branch(page0, page1, page2, Page(terminal=True))
    branch = Branch(page1, page2, Page(terminal=True))
    Compile.f(page1, page0=lab)
    Compile.f(page2, page0=lab)
    branch.pages.insert(0, page0)
    return branch

@Compile.register
def f(page, page0):
    pass
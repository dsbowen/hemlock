"""Workers"""

from hemlock import *

@Navigate.register
def Workers(origin=None):
    b = Branch(navigate_worker=True)
    Navigate.End(b)
    
    p = Page(b)
    Label(
        p,
        label="""
        <p>Sometimes a compile, validate, submit, or navigate function will take a while (10+ seconds) to run.</p>
        <p>You can use a `Worker` to show participants a loading page while these functions are processed by a Redis Queue.</p>
        <p>Active a worker by settings a `Page`'s `compile_worker`, 'validate_worker`, etc. attribute to `True`.</p>
        """
    )

    p = Page(b, compile_worker=True)
    l = Label(
        p,
        label="""
        <p>This page's compile worker will run every time the page is compiled. Refresh the page and notice the compile worker running again.</p>
        <p>To prevent this on the next page, we set `cache_compile` to `True`. This clears the compile worker and all compile functions.</p>
        """
    )

    p = Page(b, compile_worker=True, cache_compile=True)
    l = Label(
        p,
        label='<p>Refresh this page and notice that it does not run a compile worker.</p>'
    )

    return b
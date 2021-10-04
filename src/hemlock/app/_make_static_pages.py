from flask.templating import render_template


def make_loading_page() -> str:
    """Loading page."""
    from ..page import Page

    return render_template("hemlock/utils/loading_page.html", page=Page())


def make_restart_page() -> str:
    """Restart page."""
    from ..page import Page
    from ..questions import Label

    return Page(
        Label(
            """
            You have already started this survey. Click "Resume" to pick up where you 
            left off or "Restart" to start the survey from the beginning.

            If you restart the survey, your responses will not be saved.
            """
        ),
        back="Resume",
        forward="Restart",
    ).render()


def make_screenout_page() -> str:
    """Screenout page."""
    from ..page import Page
    from ..questions import Label

    return Page(
        Label(
            """
            Our records indicate that you have already participated in this or similar 
            surveys.
            
            Thank you for your continuing interest in our research!
            """
        ),
        back=False,
        forward=False,
    ).render()


def make_500_page() -> str:
    """Internal server error page."""
    from ..page import Page
    from ..questions import Label

    return Page(
        Label(
            """
            The application encountered an error. Please contact the survey 
            administrator.

            We apologize for the inconvenience and thank you for your patience as we 
            work to resolve this issue.
            """
        ),
        back=False,
        forward=False,
    ).render()

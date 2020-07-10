"""# Debugger

The debugger sends 'AI participants' through the survey. The AI 
participants attempt to break the survey by clicking random objects and 
entering random responses.

Examples
--------
This example debugs an app locally.

In `survey.py`:

```python
from hemlock import Branch, Page, Label, route

@route('/survey')
def start():
\    x = 1/0
\    return Branch(Page(Label('<p>Hello World</p>'), terminal=True))
```

In `app.py`:

```python
import survey

from hemlock import create_app

app = create_app()

if __name__ == '__main__':
\    from hemlock.app import socketio
\    socketio.run(app)
```

Open a terminal and run the app with:

```
$ python app.py $ or python3 app.py
```

Open a second terminal and open the python shell with:

```
$ python # or python3
```

Run the debugger in the second terminal:

```
>>> from hemlock.debug import AIParticipant, debug
>>> debug()
```

The debugger will open a chromedriver and attempt to complete the survey. The
first terminal window will display this error:

```
File "/home/<username>/hemlock/survey.py", line 9, in start
\    x = 1/0
ZeroDivisionError: division by zero
```

Notes
-----
If your app is running on a different local host port than 5000, set the url 
root as an environment variable before opening the python shell in your second
terminal:

```
$ export ULR_ROOT=http://localhost:xxxx
```

If your application import is not `app.app`, set the import as an enviornment
variable before opening the python shell in your second terminal:

```
$ export APP_IMPORT=path.to.app
```

AI participants run in batches of specified sizes. For local debugging, I 
recommend a batch size of 1. For production debugging, you can safely go up 
to 3.
"""

from ..models import Participant, Page
from ..tools import chromedriver

import os
import sys
import unittest
import warnings
from pydoc import locate
from threading import Thread
from time import sleep

SERVER_ERR = 'Internal Server Error'
WERKZEUG_ERR = "Brought to you by DON'T PANIC, your friendly Werkzeug powered traceback interpreter."
ERROR_MSG = "{ai.part} encountered an error. \n\nDon't give up."

def debug(num_batches=1, batch_size=1):
    """
    Run the debugger.

    Parameters
    ----------
    num_batches : int, default=1
        Number of batches of AI participants to run.

    batch_size : int, default=1
        Number of AI participants to run per batch.

    Returns
    -------
    result : bool
        `True` if all AI participants in all batches run sucessfully.
        Otherwise, the program will crash.

    Notes
    -----
    When called from the command line tool, `num_batches` and `batch_size` are
    passed as strings.
    """
    results = [run_batch(int(batch_size)) for i in range(int(num_batches))]
    return all(results)

def run_batch(batch_size=1):
    """
    Run a batch of AI participants.
    
    Parameters
    ----------
    batch_size : int, default=1
        Number of AI participants to run in this batch.

    Returns
    -------
    result : bool
        `True` if all AI participants in this batch run successfully. 
        Otherwise, the program will crash.
    """
    threads = [
        SuccessThread(target=run_participant, daemon=True)
        for i in range(batch_size)
    ]
    [t.start() for t in threads]
    [t.join() for t in threads]
    if not all([t.success for t in threads]):
        sys.exit()
    return True

def run_participant():
    """
    Run a single AI participant through the survey. Assert that the
    participant does not encounter failures or errors.

    Returns
    -------
    result : bool
        `True` if the participant ran successfully.
    """
    result = unittest.main(exit=False).result
    assert not result.failures and not result.errors
    return True


class AIParticipant(unittest.TestCase):
    def setUp(self):
        """Push application context and connect webdriver"""
        warnings.simplefilter('ignore', ResourceWarning)
        sys.path.insert(0, os.getcwd())
        app = locate(os.environ.get('APP_IMPORT') or 'app.app')
        sys.path.pop(0)
        self.ctx = app.app_context()
        self.ctx.push()
        self.driver = chromedriver()
        url_root = os.environ.get('URL_ROOT') or 'http://localhost:5000'
        self.driver.get(url_root+'?Test=1')
        self.part = Participant.query.all()[-1]
        super().setUp()

    def test(self):
        """An AI Participant has encountered an error."""
        current_page = self.get_current_page()
        while current_page is None or not current_page.terminal:
            self.check_for_error()
            if current_page is None:
                self.driver.refresh()
                sleep(3)
            else:
                print('Debugging page ', current_page, current_page.name)
                current_page._debug(self.driver)
            current_page = self.get_current_page()

    def get_current_page(self):
        """Get the current page"""
        try:
            while True:
                # accept all alerts at the start of the page
                self.driver.switch_to.alert.accept()
        except:
            pass
        try:
            page_tag = self.driver.find_element_by_tag_name('page')
        except:
            return None
        page_id = page_tag.get_attribute('id').split('-')[-1]
        return Page.query.get(page_id)

    def check_for_error(self):
        """Assert that there are no errors on this page"""
        error = False
        try:
            h1 = self.driver.find_element_by_tag_name('h1')
            error = h1.text == SERVER_ERR
        except:
            pass
        try:
            footer = self.driver.find_element_by_css_selector('div.footer')
            error = error or footer.text == WERKZEUG_ERR
        except:
            pass
        assert not error, ERROR_MSG.format(ai=self)

    def tearDown(self):
        """Close webdriver and pop application context"""
        self.driver.close()
        self.ctx.pop()
        super().tearDown()


class SuccessThread(Thread):
    """Operates as normal thread with success indicator"""
    def run(self):
        try:
            super().run()
            self.success = True
        except:
            self.success = False
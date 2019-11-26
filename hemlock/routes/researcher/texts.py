"""Texts for researcher routes"""

from hemlock.app.settings_utils import FORWARD_BUTTON_TEMPLATE

from flask import Markup

PASSWORD_PROMPT = '<p>Please enter your password.</p>'

PASSWORD_INCORRECT = 'The password you entered was incorrect.'

LOGIN_REQUIRED = 'Login required to access this page.'

LOGIN_BUTTON = Markup(
    FORWARD_BUTTON_TEMPLATE.format(classes='w-100', text='Login')
)

PARTICIPANTS = """
<table align="center" style="width:50%">
    <tr>
        <th style="text-align:center" colspan="2">Participants' Current Status</th>
    </tr>
    <tr><td colspan="2"><hr/></td></tr>
    <tr>
        <td>Completed</td>
        <td id="Completed" align="right">{Completed}</td>
    </tr>
    <tr>
        <td>In Progress</td>
        <td id="InProgress" align="right">{InProgress}</td>
    </tr>
    <tr>
        <td>Timed Out</td>
        <td id="TimedOut" align="right">{TimedOut}</td>
    </tr>
    <tr>
        <td>Total</td>
        <td id="Total" align="right">{Total}</td>
    </tr>
</table>
"""

SELECT_FILES_TXT = "<p>Select files to download.</p>"

SURVEY_VIEW_TXT = "<p>Enter participant IDs for survey viewing.</p>"

INVALID_ID = "<p>The following participant ID was invalid: {}."

INVALID_IDS = "<p>The following participant IDs were invalid: {}."
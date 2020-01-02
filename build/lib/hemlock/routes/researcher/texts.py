"""Texts for researcher routes"""

from flask import Markup

PASSWORD_PROMPT = '<p>Please enter your password.</p>'

PASSWORD_INCORRECT = 'The password you entered was incorrect.'

LOGIN_REQUIRED = 'Login required to access this page.'

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

EMPTY_DATAFRAME = "No data are available to create the profle."

PROFILE_CREATION_ERR = '''
<p>An error occurred while creating the data profile.</p>
<p>Check that you have enabled background jobs.</p>
'''
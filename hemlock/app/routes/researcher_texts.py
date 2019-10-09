"""Texts for researcher routes"""

from hemlock.app.setting_utils import FORWARD_BUTTON_TEMPLATE

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
        <td id="completed" align="right">{completed}</td>
    </tr>
    <tr>
        <td>In Progress</td>
        <td id="in_progress" align="right">{in_progress}</td>
    </tr>
    <tr>
        <td>Timed Out</td>
        <td id="timed_out" align="right">{timed_out}</td>
    </tr>
    <tr>
        <td>Total</td>
        <td id="total" align="right">{total}</td>
    </tr>
</table>
"""

DOWNLOAD = "<p>Select files to download.</p>"

DOWNLOAD_BUTTON = Markup(
    FORWARD_BUTTON_TEMPLATE.format(classes='w-100', text='Download')
)
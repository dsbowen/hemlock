PASSWORD_PROMPT = '<p>Please enter your password.</p>'

PASSWORD_INCORRECT = '<p>The password you entered was incorrect.</p>'

LOGIN_REQUIRED = 'Login required to access this page.'

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
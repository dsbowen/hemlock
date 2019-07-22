##############################################################################
# Html texts
# by Dillon Bowen
# last modified 07/21/2019
##############################################################################



##############################################################################
# Navigation
##############################################################################

BREAK = '''
    <br>
'''

FORWARD_BUTTON = '''
    <button id='forward-button' name='direction' type='submit' class='btn btn-primary' style='float: right;' value='forward'>
    >> 
    </button>
'''

BACK_BUTTON = '''
    <button id='back-button' name='direction' type='submit' class='btn btn-primary' style='float: left;' value='back'> 
    << 
    </button>
'''

PAGE_BREAK = '''
    <br style='line-height:3;'></br>
'''



##############################################################################
# Question
##############################################################################

QUESTION = '''
    <div class='{0}'>
    {1}
    </div>
'''

DIV = '''
        <label for='{0}'>
        {1}
        </label>
        {2}
'''

ERROR = '''
        <span style='color:red'>{0}</span>
'''

FREE = '''
        <input type='text' class='form-control' id='{0}' name='{0}' value='{1}'>
'''

CHOICE = '''
        <div class='radio'>
            <label class='span'>
            <input type='radio' name='{0}' value='{1}' {2}>
            {3}
            </label>
        </div>
'''
"""Function for compiling Page html"""

PAGE_BODY = """
    {question_html}
    <br>
    {submit_html}
    <br style="line-height:3;"></br>
"""

FORWARD_BUTTON = """
    <button id="forward-button" name="direction" type="submit" class="btn btn-outline-primary" style="float: right;" value="forward">
    >> 
    </button>
"""

BACK_BUTTON = """
    <button id="back-button" name="direction" type="submit" class="btn btn-outline-primary" style="float: left;" value="back"> 
    << 
    </button>
"""

def compile_page_body(page):
    question_html = ''.join([q._compile_html() for q in page.questions])
    submit_html = ''
    if page.back:
        submit_html += BACK_BUTTON
    if page.forward and not page.terminal:
        submit_html += FORWARD_BUTTON
    return PAGE_BODY.format(
        question_html=question_html, submit_html=submit_html)
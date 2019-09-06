##############################################################################
# Hemlock survey template
# by Dillon Bowen
# last modified 07/24/2019
##############################################################################

# import hemlock package, configuration class, and texts
from hemlock import *
from custom_compilers import *
from debug import AIParticipant as AIP
from config import Config
from texts import *
from flask_login import current_user

def Start():
    raise NotImplementedError()
    
table = '''
<center>
<table style="margin-left: auto; margin-right: auto; border-collapse: collapse;" border="1px">
<tbody>
<tr style="height: 35px;">
<td style="text-align: center;" colspan="3">Export to Word</td>
<tr style="height: 35px;">
<td style="text-align: center; width: 130px;"></td>
<td style="text-align: center; width: 130px;">Hemlock</td>
<td style="text-align: center; width: 130px;">Qualtrics</td>
</tr>
<tr style="height: 35px;">
<td style="text-align: center;">Local images</td>
<td style="text-align: center;">Yes</td>
<td style="text-align: center;">Yes</td>
</tr>
<tr style="height: 35px;">
<td style="text-align: center;">Images from URL</td>
<td style="text-align: center;">Yes</td>
<td style="text-align: center;">Yes</td>
</tr>
<tr style="height: 35px;">
<td style="text-align: center;">Videos</td>
<td style="text-align: center;">Yes</td>
<td style="text-align: center;">No</td>
</tr>
<tr style="height: 35px;">
<td style="text-align: center;">Tables</td>
<td style="text-align: center;">Yes</td>
<td style="text-align: center;">No</td>
</tr>
</tbody>
</table>
</center>
'''
        
def Start():
    b = Branch()
    
    p = Page(b)
    q = Question(p, '<p>This image is local</p>')
    img = image(src='wanna_see_the_code.png', classes=['fit', 'center'])
    q = Question(p, img)
    
    p = Page(b)
    q = Question(p, '<p>This image is from a url</p>')
    url = "https://imgs.xkcd.com/comics/wanna_see_the_code_2x.png"
    img = image(src=url, classes=['fit', 'center'], copy_for_viewing=True)
    q = Question(p, img)
    
    p = Page(b)
    video_q = Question(
        p, '<p>Input the link to your favorite YouTube video</p>', 
        qtype='free')
    
    p = Page(b)
    q = Question(p, compile=get_video, compile_args={'video_q': video_q})
    
    p = Page(b)
    q = Question(p, table)
    
    p = Page(b, terminal=True)
    q = Question(p, 'Take note! Your ID is {}'.format(current_user.id))
    return b
    
def get_video(q, video_q):
    url = video_q.get_response()
    q.text(video(url, parms={'autoplay':1}))
    
def Start():
    b = Branch()
    p = Page(b, terminal=True)
    q = Question(p, 'hello world')
    return b
    
def compile(q, hello):
    q.text('hello '+hello)
      
# create the application (survey)
app = create_app(
    Config,
    start=Start,
    password='',
    record_incomplete=False,
    block_duplicate_ips=False,
    block_from_csv='block.csv',
    debug=True)
    
# run app
if __name__ == '__main__':
    app.run()
    
# hemlock shell
import hemlock_shell

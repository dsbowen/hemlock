"""Hemlock survey"""

from hemlock import *
from texts import *

def Start(root=None):
    b = Branch()
    Navigate(b, End)

    p = Page(b)
    img_url = 'https://imgs.xkcd.com/comics/wanna_see_the_code.png'
    img = Img(url=img_url, classes=['fit'])
    Text(p, text=img.render())

    p = Page(b)
    img = Img(filename='wanna_see_the_code.png', classes=['fit'])
    Text(p, text=img.render())

    p = Page(b)
    vid_url = 'https://www.youtube.com/watch?v=bRhg2zvalXc'
    vid = YouTubeVid(url=vid_url, parms={'autoplay': 1})
    Text(p, text=vid.render())
    
    return b

def End(root):
    b = Branch()
    p = Page(b, terminal=True)
    Text(p, text='Goodbye World')
    return b
"""Hemlock survey"""

from hemlock import *
from texts import *

def Start(root=None):
    b = Branch()
    Navigate(b, End)

    p = Page(b)
    img = Img(
        filename='wanna_see_the_code.png', 
        bucket='hemlock-bucket',
        classes=['fit']
    )
    Text(p, text=img.render())

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

    p = Page(b)
    mc = MultiChoice(p, text="<p>Which of these do you like?</p>", var='FavoriteVid')
    sabaton_url = 'https://www.youtube.com/watch?v=bRhg2zvalXc'
    sabaton = YouTubeVid(url=sabaton_url)
    Choice(mc, text=sabaton.render(), label='Sabaton', value='Sabaton')

    caravan_url = 'https://www.youtube.com/watch?v=cq3fwlZdWhw'
    caravan = YouTubeVid(url=caravan_url)
    Choice(mc, text=caravan.render(), label='CaravanPalace', value='CaravanPalace')

    keane_url = 'https://www.youtube.com/watch?v=Zx4Hjq6KwO0'
    keane = YouTubeVid(url=keane_url)
    Choice(mc, text=keane.render(), label='Keane', value='Keane')
    
    return b

def End(root):
    b = Branch()
    p = Page(b, terminal=True)
    Text(p, text='Goodbye World')
    return b
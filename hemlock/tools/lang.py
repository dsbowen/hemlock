"""Language tools"""

def indef_article(string):
    return 'an' if string[0] in 'aeiou' else 'a'

def plural(val, singular, plural=None):
    return singular if val==1 else (plural or singular+'s')
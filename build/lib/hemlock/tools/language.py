"""Language tools"""

def plural(val, plur='s', sing=''):
    return sing if val==1 else plur
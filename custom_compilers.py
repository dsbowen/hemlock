##############################################################################
# Custom html compile functions template
# by Dillon Bowen
# last modified 08/14/2019
##############################################################################

from hemlock import compiler

@compiler.register('custom question type')
def custom_compile_function(q):
    return 'custom html'
from docstr_md.python import PySoup, compile_md
from docstr_md.src_href import Github

import os

src_href = Github('https://github.com/dsbowen/hemlock/blob/master')

# application and settings
path = 'hemlock/app/__init__.py'
soup = PySoup(path=path, parser='sklearn', src_href=src_href)
path = 'hemlock/app/settings.py'
soup.objects += PySoup(path=path, parser='sklearn', src_href=src_href).objects
compile_md(soup, compiler='sklearn', outfile='docs_md/app.md')

# debugging
path = 'hemlock/debug/__init__.py'
soup = PySoup(path=path, parser='sklearn', src_href=src_href)
soup.keep_objects('debug', 'run_batch', 'run_participant')
compile_md(soup, compiler='sklearn', outfile='docs_md/debug.md')

# functions
function_filenames = ['compile', 'debug', 'submit', 'validate']
for filename in function_filenames:
    path = os.path.join('hemlock/functions', filename+'.py')
    soup = PySoup(path=path, parser='sklearn', src_href=src_href)
    outfile = os.path.join('docs_md', filename+'_functions.md')
    compile_md(soup, compiler='sklearn', outfile=outfile)

# models
def mod_base_soup(soup):
    soup.rm_objects('BranchingBase')

def mod_page_soup(soup):
    soup.keep_objects('Page')

modifications = {
    'bases': mod_base_soup,
    'page': mod_page_soup,
}

model_filenames = [
    'bases',
    'branch',
    'choice',
    'embedded',
    'functions',
    'navbar',
    'page',
    'participant',
    'question',
    'workers',
]

for filename in model_filenames:
    path = os.path.join('hemlock/models', filename+'.py')
    soup = PySoup(path=path, parser='sklearn', src_href=src_href)
    soup.import_path = 'hemlock'
    soup.rm_properties()
    func = modifications.get(filename)
    if func:
        func(soup)
    outfile = os.path.join('docs_md', filename+'.md')
    compile_md(soup, compiler='sklearn', outfile=outfile)

# tools
tools_filenames = [
    'comprehension',
    'lang',
    'random',
    'statics',
    'url_for',
    'webdriver',
]

for filename in tools_filenames:
    path = os.path.join('hemlock/tools', filename+'.py')
    soup = PySoup(path=path, parser='sklearn', src_href=src_href)
    soup.import_path = 'hemlock/tools'
    soup.rm_properties()
    outfile = os.path.join('docs_md', filename+'.md')
    compile_md(soup, compiler='sklearn', outfile=outfile)
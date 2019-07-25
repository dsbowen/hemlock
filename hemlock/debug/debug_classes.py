##############################################################################
# Debug classes
# by Dillon Bowen
# last modified 07/24/2019
##############################################################################

from ast import literal_eval

class DebugPage():
    def __init__(self, driver):
        page = driver.find_element_by_tag_name('page')
        self.debug = page.get_attribute('debug')
        self.args = literal_eval(page.get_attribute('args'))
        attrs = literal_eval(page.get_attribute('attrs'))
        [setattr(self, name, value) for name, value in attrs.items()]
        
##############################################################################
# Debug classes
# by Dillon Bowen
# last modified 07/24/2019
##############################################################################

from ast import literal_eval

class DebugBase():
    def _debug_init(self, AIP, default_debug, elem):
        self._get_debug(AIP, default_debug, elem)
        self._get_debug_args(elem)
        self._get_attrs(elem)
    
    def _get_debug(self, AIP, default_debug, elem):
        try:
            self._debug = getattr(AIP, elem.get_attribute('debug'))
        except:
            self._debug = default_debug
    
    def _get_debug_args(self, elem):
        try:
            self._args = literal_eval(elem.get_attribute('args'))
        except:
            self._args = None
    
    def _get_attrs(self, elem):
        try:
            attrs = literal_eval(elem.get_attribute('attrs'))
            [setattr(self, name, value) for name, value in attrs.items()]
        except:
            pass
    
    def debug(self):
        if self._args is None:
            return self._debug(self)
        return self._debug(self, **self._args)
        

class DebugPage(DebugBase):
    def __init__(self, AIP):
        page_elem = AIP.driver.find_element_by_tag_name('page')
        self._debug_init(AIP, AIP._default_page_debug, page_elem)
        self._get_questions(AIP)
    
    def _get_questions(self, AIP):
        question_elems = AIP.driver.find_elements_by_class_name('question')
        self.questions = [DebugQuestion(AIP, elem) for elem in question_elems]

class DebugQuestion(DebugBase):
    def __init__(self, AIP, question_elem):
        self._debug_init(AIP, AIP._default_question_debug, question_elem)
        self._get_inputs(AIP, question_elem)
    
    def _get_inputs(self, AIP, question_elem):
        inputs = question_elem.find_elements_by_tag_name('input')
        
        text_entry = [i for i in inputs 
            if i.get_attribute('type') == 'text']
        self.text_entry = text_entry[0] if len(text_entry)==1 else text_entry
        print('get input text entry:', self.text_entry)
        
        self.choices = [DebugChoice(AIP, i) for i in inputs 
            if i.get_attribute('type') == 'radio']

class DebugChoice(DebugBase):
    def __init__(self, AIP, elem):
        pass
    
    
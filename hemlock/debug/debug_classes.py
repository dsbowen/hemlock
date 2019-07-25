##############################################################################
# Debug classes
# by Dillon Bowen
# last modified 07/24/2019
##############################################################################

from ast import literal_eval

# Debug Base class
class DebugBase():
    # Initializes debug class with debug function, arguments, and attributes
    def _debug_init(self, AIP, default_debug, elem):
        self._get_debug(AIP, default_debug, elem)
        self._get_debug_args(elem)
        self._get_attrs(elem)
    
    # Get debug function
    def _get_debug(self, AIP, default_debug, elem):
        try:
            self._debug = getattr(AIP, elem.get_attribute('debug'))
        except:
            self._debug = default_debug
    
    # Get debug function arguments
    def _get_debug_args(self, elem):
        try:
            self._args = literal_eval(elem.get_attribute('args'))
        except:
            self._args = None
    
    # Get attributes of debug class
    def _get_attrs(self, elem):
        try:
            attrs = literal_eval(elem.get_attribute('attrs'))
            [setattr(self, name, value) for name, value in attrs.items()]
        except:
            pass
    
    # Call debug function
    def debug(self):
        if self._args is None:
            return self._debug(self)
        return self._debug(self, **self._args)
        
# Debug Page class
class DebugPage(DebugBase):
    def __init__(self, AIP):
        page_elem = AIP.driver.find_element_by_tag_name('page')
        self._debug_init(AIP, AIP._default_page_debug, page_elem)
        self._get_questions(AIP)
    
    # Get questions
    def _get_questions(self, AIP):
        question_elems = AIP.driver.find_elements_by_class_name('question')
        self.questions = [DebugQuestion(AIP, self, elem) 
            for elem in question_elems]

# Debug Question class
class DebugQuestion(DebugBase):
    def __init__(self, AIP, page, question_elem):
        self.page = page
        self._debug_init(AIP, AIP._default_question_debug, question_elem)
        self._get_inputs(AIP, question_elem)
    
    # Get inputs
    # inputs may be a text entry box or choices
    def _get_inputs(self, AIP, question_elem):
        inputs = question_elem.find_elements_by_tag_name('input')
        
        text_entry = [i for i in inputs 
            if i.get_attribute('type') == 'text']
        self._text_entry = text_entry[0] if len(text_entry)==1 else text_entry
        
        self.choices = [DebugChoice(AIP, self, i) for i in inputs 
            if i.get_attribute('type') == 'radio']
    
    # Send keys to text entry box
    def send_keys(self, keys):
        try:
            self._text_entry.send_keys(keys)
        except:
            pass
    
    # Clear text entry box
    def clear(self):
        try:
            self._text_entry.clear()
        except:
            pass

# Debug Choice class
class DebugChoice(DebugBase):
    def __init__(self, AIP, question, choice_elem):
        self.question = question
        self._debug_init(AIP, AIP._default_choice_debug, choice_elem)
        self._button = choice_elem

    # Click on the choice
    def click(self):
        self._button.click()
    
    
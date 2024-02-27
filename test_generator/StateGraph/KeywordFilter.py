from os.path import join, dirname
ASSERT_KEYWORD_PATH = join(dirname(__file__), './Data/assertion.txt')
ACTION_KEYWORD_PATH = join(dirname(__file__), './Data/action.txt')

class KeywordFilter:
    with open(ASSERT_KEYWORD_PATH, 'r') as file:
        assertion = file.read().split('\n')
    
    with open(ACTION_KEYWORD_PATH, 'r') as file:
        action = file.read().split('\n')

    @classmethod
    def is_assertion(cls, keyword):
        return keyword in cls.assertion

    @classmethod
    def is_action(cls, keyword):
        return keyword in cls.action
    
    @classmethod
    def get_type(cls, step):
        if cls.is_assertion(step.action):
            return 'Assertion'
        # Remove for from the special keywords. Consider for is an atomic action
        special_keywords = ['If', 'Try', 'While', 'Do-while', 'Else']
        if step.action in special_keywords:
            return step.action
        return 'Action'

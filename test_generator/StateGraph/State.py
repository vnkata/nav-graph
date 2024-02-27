import json
import CodeConverter
from TestStep import TestStep
class AbstractState:
    pass

class State(AbstractState):
    def __init__(self, prev_action=None, cur_action=None, assertion=None, other_condition=None) -> None:
        self.prev_action = prev_action
        self.cur_action = cur_action
        self.assertions = assertion if assertion is not None else []
        self.other_condition = other_condition # This could be if, for, while loop, etc

    def __eq__(self, other):
        if isinstance(other, State):
            return self.cur_action == other.cur_action  \
                and self.assertions == other.assertions 
        return False 

    def __hash__(self) -> int:
        return hash((self.cur_action, tuple(self.assertions), self.other_condition))

    def __str__(self) -> str:
        return self.toJSON()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class MasterState(AbstractState):
    id = 0
    def __init__(self, prev_action=None, cur_action: 'TestStep'=None, tag=None, assertions=[], child_state=[]) -> None:
        self.prev_action = prev_action
        self.cur_action = cur_action
        self.assertions = assertions
        self.tag = tag # This could be if, for, while loop, etc
        self.child_state = child_state 
        self.test_id = set()
        self.version_id = 0
        self.id = MasterState.id
        MasterState.id += 1
        #print(self.id)

    def __eq__(self, other):
        if isinstance(other, MasterState):
            # return self.prev_action == other.prev_action \
            #     and self.cur_action == other.cur_action  \
            return self.cur_action == other.cur_action    \
                and self.assertions == other.assertions   \
                and self.tag == other.tag                 \
                and self.child_state == other.child_state \
                and self.id == other.id
                # and self.version_id == other.version_id
        return False 

    def __hash__(self) -> int:
        # return hash((self.prev_action, self.cur_action, tuple(self.assertions), self.tag, tuple(self.child_state), self.version_id))
        # return hash((self.cur_action, tuple(self.assertions), self.tag, tuple(self.child_state), self.version_id))
        return hash((self.cur_action, tuple(self.assertions), self.tag, tuple(self.child_state), self.id))
        
    def __str__(self) -> str:
        return self.toJSON()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def get_description(self):
        action = self.cur_action.to_code() if self.cur_action else ''
        assertions = ', '.join([assertion.to_code() for assertion in self.assertions if assertion])
        return 'TestID: {} Action: {} Assertion: {}'.format(self.test_id, action, assertions)

    def similar(self, other):
        """
            2 states are similar if they are only different in version_id
        """
        if isinstance(other, MasterState):
            # return self.prev_action == other.prev_action \
            #     and self.cur_action == other.cur_action  \
            return self.cur_action == other.cur_action   \
                and self.assertions == other.assertions  \
                and self.tag == other.tag                \
                and self.child_state == other.child_state 
        return False 
    
    def to_code(self):
        return CodeConverter.CodeConverter.convert_one(self)
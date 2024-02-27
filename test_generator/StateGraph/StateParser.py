from copy import deepcopy
from os.path import dirname, join

from KeywordFilter import KeywordFilter
from Graph import Graph
from TestStep import TestStep
from State import MasterState

class StateParser():
    with open(join(dirname(__file__), './Data/skip.txt'), 'r') as file:
        skiped_action = file.readlines()
    skiped_action = [command.strip() for command in skiped_action]

    def __init__(self) -> None:
        pass
    
    @classmethod
    def parse_a_testcase(cls, filename):
        MasterState.id = 0
        with open(filename, 'r') as file:
            file_content = file.read().strip()
        steps_json = file_content.split('\n')
        # steps = [TestStep.from_json(content) for content in steps_json]
        steps = []
        for content in steps_json:
            # print(content)
            step = TestStep.from_json(content)
            if step.action in cls.skiped_action:
                continue
            steps.append(TestStep.from_json(content))
        return StateParser.parse(steps, filename)

    @staticmethod
    def parse(steps, filename=None):
        current_step = None
        prev_state = None
        cur_state = MasterState()
        graph = Graph()
        i = 0

        def parse_action():
            nonlocal current_step, prev_state, cur_state, graph, i
            prev_state = deepcopy(cur_state)
            cur_state = MasterState(prev_action=prev_state.cur_action, \
                    cur_action=current_step, assertions=[])
            
            while i + 1 < len(steps) and KeywordFilter.get_type(steps[i + 1]) == 'Assertion':
                current_step = steps[i + 1]
                parse_assertion()
                i += 1
            
            # print(prev_state) 
            # print(cur_state)
            graph.insert((deepcopy(prev_state), deepcopy(cur_state)))

        def parse_assertion():
            nonlocal current_step, cur_state
            cur_state.assertions.append(deepcopy(current_step))
            # print(f"Assert: {cur_state}")
        
        def parse_if():
            nonlocal current_step, prev_state, cur_state, graph, i, steps
            
            prev_state = deepcopy(cur_state)
            cur_state = MasterState(prev_action=prev_state.cur_action, 
                            tag=KeywordFilter.get_type(current_step),
                            child_state=[current_step])
            if i + 1 < len(steps) and KeywordFilter.get_type(steps[i+1]) == 'Else':
                cur_state.child_state.append(steps[i+1])
                i += 1

            while i + 1 < len(steps) and KeywordFilter.get_type(steps[i + 1]) == 'Assertion':
                current_step = steps[i + 1]
                parse_assertion()
                i += 1
            cur_state = MasterState(prev_action = prev_state.cur_action, 
                                    cur_action = cur_state, 
                                    assertions=cur_state.assertions)
            graph.insert((deepcopy(prev_state), deepcopy(cur_state)))


        def parse_master():
            nonlocal current_step, prev_state, cur_state, graph, i
            # print(prev_state, cur_state)
            
            prev_state = deepcopy(cur_state)
            cur_state = MasterState(prev_action=prev_state.cur_action, 
                            tag = current_step.action,
                            child_state=[current_step])
            while i + 1 < len(steps) and KeywordFilter.get_type(steps[i + 1]) == 'Assertion':
                current_step = steps[i + 1]
                parse_assertion()
                i += 1
            graph.insert((deepcopy(prev_state), deepcopy(cur_state)))

        switcher = {'Action': parse_action, 'If': parse_if, 'Assertion': parse_assertion}
        while i < len(steps):
            current_step = steps[i]
            action_type = KeywordFilter.get_type(steps[i])
            # print(f'Type: {action_type}')
            switcher.get(action_type, parse_master)()
            i += 1
        # graph.insert((prev_state, cur_state))
        # print('=' * 30)
        # graph.summary('Visualize/' + filename.split('\\')[-1].replace('.txt', '.html'))
        # print('=' * 30)
        nodes = list(graph.vertex.keys())
        return graph

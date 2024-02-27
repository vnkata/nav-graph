from TestStep import TestStep
import Graph
from State import State
from copy import deepcopy
from typing import Tuple
from KeywordFilter import KeywordFilter

class StateParser:
    def __init__(self) -> None:
        pass

    @staticmethod
    def parse_a_testcase(filename) -> Graph:
        with open(filename, 'r') as file:
            file_content = file.read()
        steps_json = file_content.split('\n')
        steps = [TestStep.from_json(content) for content in steps_json]
        return StateParser.parse(steps, State())

    @staticmethod
    def parse(steps, first_node) -> Tuple[Graph.Graph, State]:  
        previous_action = None
        current_action = None
        prev_state = first_node
        cur_state = State(prev_action=first_node.cur_action)
        sub_graph = Graph.Graph(first_node)
        i = 0

        # Some what complete
        def parse_action():
            print("Parse action")
            nonlocal previous_action, cur_state, previous_action, prev_state
            cur_state.cur_action = current_action
            sub_graph.insert((prev_state, cur_state))
            previous_action = current_action
            prev_state = cur_state
            cur_state = State(prev_action=previous_action)

        # Complete
        def parse_asserts():
            nonlocal previous_action, cur_state, previous_action, prev_state
            print("Parse assertion")
            cur_state.assertions.append(current_action)

        def parse_block():
            nonlocal previous_action, cur_state, previous_action, prev_state
            print("Parse block statement")
            cur_state = deepcopy(prev_state)
            cur_state.other_condition = current_action.get_condition()
            sub_graph.insert((prev_state, cur_state))
            
            child_graph, prev_state = StateParser.parse(current_action.child, cur_state)
            cur_state = State(prev_action=prev_state.cur_action, other_condition="End block")
            child_graph.insert((prev_state, cur_state))
            prev_state = cur_state

            sub_graph.merge(child_graph)

        # TODO: Something not right.
        def parse_if():
            nonlocal current_action, cur_state, previous_action, prev_state, i
            print("Parse if statement")
            condition = current_action.get_condition()
            branch_state = deepcopy(prev_state)

            parse_block()
            if i + 1 < len(steps) and steps[i + 1].action == 'Else':
                prev_state = branch_state
                current_action = steps[i + 1]

        def parse_try_catch():
            nonlocal previous_action, cur_state, previous_action, prev_state
            print("Parse try catch statement")
            pass

        switches = {'Action': parse_action, 
                    'Assertion': parse_asserts, 
                    'Try': parse_try_catch, 
                    'If': parse_if, 
                    'While': parse_block,
                    'For': parse_block}

        while i < len(steps):
            current_action = steps[i]
            # print(previous_action)
            step_type = KeywordFilter.get_type(current_action)
            switches[step_type]()
            i += 1
            print(i)
        return sub_graph, prev_state


g, end = StateParser.parse_a_testcase("GroovyParser/Output/input.txt")
t = list(g.vertex.keys())
g.summary()

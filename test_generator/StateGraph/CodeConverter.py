from TestStep import TestStep
from typing import ContextManager, List
import State 
class CodeConverter:
    
    def __init__(self) -> None:
        pass
    
    @staticmethod
    def convert_normal(state: State.MasterState) -> str:
        # print('Convert normal')
        return state.cur_action.to_code()

    @staticmethod
    def convert_block_input(state: State.MasterState, prefix) -> str:
        '''
            Convert to prefix + input + { block } structure           
            E.g: if (condition) { block }
                 while (condition) { block }
        '''
        # print('Convert block input')
        action = state.cur_action
        code = prefix + action.input.to_code() + '{ '
        block = CodeConverter.convert_steps(state.child_state)
        code += block + ' }'
        return code

    @staticmethod
    def convert_block(state: State.MasterState, prefix: str) -> str:
        '''
            Convert to prefix + { block } structure
            E.g: else { block }, try { block }
        '''
        # print('Convert block')
        code = prefix + '{ '
        block = CodeConverter.convert_steps(state.child_state)
        code += block + ' }'
        return code
    
    @staticmethod
    def convert_assignment(state: State.MasterState) -> str:
        # print('Convert assignment')
        lhs = [term.to_code() for term in state.cur_action.output]
        rhs = [term.to_code() for term in state.cur_action.input]
        return ','.join(lhs) + ' = ' + ','.join(rhs)

    @staticmethod
    def convert_if(state: State.MasterState) -> str:
        # print("Convert if")
        code = ''
        step = state.child_state[0]
        code += 'if ' + step.input[0].to_code() + '{\n' + CodeConverter.convert_steps(step.child) + '}'
        if len(state.child_state) == 2 and state.child_state[1].action == 'Else':
            # print(state.child_state[1], TestStep())
            step = state.child_state[1]
            code += '\n else { \n' + CodeConverter.convert_steps(step.child) + '}'
        return code

    @staticmethod
    def convert_one(state: State.MasterState) -> str:
        source_code = ''
        if not state.cur_action and not state.tag: 
            return ''

        #normal command
        type = state.tag if state.tag else state.cur_action.action
        if type in ['Try', 'Finally']:
            switcher = {
                'Try'    : 'try ',
                'Finally': 'finally '
            }
            code = CodeConverter.convert_block(state, switcher[type])
        elif type == 'Assignment':
            code = CodeConverter.convert_assignment(state)
        elif type == 'If':
            code = CodeConverter.convert_if(state)
        elif type in ['While', 'Catch']:
            switcher = {
                'While': 'while ',
                'Catch': 'catch '
            }
            code = CodeConverter.convert_block_input(state, switcher[type])
        else:
            code = CodeConverter.convert_normal(state)
        source_code += code + '\n'
        if state.assertions != []:
            for assertion in state.assertions:
                code += assertion.to_code() + '\n'
        return code

    @staticmethod
    def convert(states: List[State.MasterState]) -> str:
        source_code = ''
        for state in states:
            code = CodeConverter.convert_one(state)
            source_code += code            
        return source_code

    @staticmethod
    def convert_steps(steps: List[TestStep]) -> str:
        code = ''
        if steps is None:
            return code
        for step in steps:
            if step:
                code += step.to_code() + '\n'
        return code

class ImportIndex:
    data = set()

    def read_import(cls, script_path):
        with open(script_path, encoding='utf-8') as file:
            content = file.read().strip().split('\n')
        imp = set()
        for line in content:
            # print('prefix', line[:6])
            if line[:6] == 'import':
                imp.add(line)
        cls.data = cls.data.union(imp)
    
    def get_imports(cls, path):
        imports = set()
        # print(cls.data)
        for node in path:
            imports = imports.union(cls.data[node.test_id])
            
        return '\n'.join(list(imports)) + '\n'
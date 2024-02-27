import json
from types import SimpleNamespace as Namespace
import re

def customDecoder(obj):
    if 'type' in obj.keys() and obj['type'] == 'Statement':
        return Statement(obj['code'])
    if 'type' in obj.keys() and obj['type'] == 'Variable':
        return Variable(obj['name'], obj['datatype'])
    if 'type' in obj.keys() and obj['type'] == 'Constant':
        return Constant(obj['value'], obj['datatype'])
    return TestStep(obj["Receiver"], obj['Action'], obj['Input'], obj['Output'], child=obj['Child'])

class Statement:
    def __init__(self, code) -> None:
        self.code = code
    
    def __eq__(self, o: object) -> bool:
        return self.code == o.code

    def __hash__(self) -> int:
        return hash(("Statement", self.code))

    def to_code(self) -> str:
        return self.code

class Variable:
    def __init__(self, name, datatype) -> None:
        self.name = name
        self.datatype = datatype
    
    def __eq__(self, o: object) -> bool:
        return self.name == o.name and self.datatype == o.datatype
    
    def __hash__(self) -> int:
        return hash(("Variable", self.name, self.datatype))
    
    def to_code(self) -> str:
        return self.name

class Constant:
    def __init__(self, value, datatype) -> None:
        self.value = value
        self.datatype = datatype

    def __eq__(self, o: object) -> bool:
        return self.value == o.value and self.datatype == o.datatype
    
    def __hash__(self) -> int:
        return hash(("Constant", self.value, self.datatype))
    
    def to_code(self) -> str:
        if self.datatype == 'java.lang.String':
            ret = re.sub("\'","\\\'",self.value)
            return "'" + ret + "'"
        else:
            return self.value


class TestStep:
    def __init__(self, receiver='', action=None, input=[], output=[], exception_handling=None, child=None) -> None:
        self.receiver = receiver
        self.action = action
        self.input = input
        self.output = output
        self.expcetion_handling = exception_handling
        self.child = child

    @staticmethod
    def from_json(content):
        return json.loads(content, object_hook=customDecoder)

    def get_action(self):
        return self.action
    
    def __str__(self) -> str:
        return self.toJSON()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

    def get_condition(self):
        if self.action == 'While':
            return f"while({self.input[0].code})"
        if self.action == "For":
            return f"for({self.input[0].code})"
    
    def __hash__(self) -> int:
        # print(self.output)
        return hash((self.receiver, self.action, tuple(self.input), tuple(self.output), self.expcetion_handling))
    
    def __eq__(self, o: object) -> bool:
        if isinstance(o, TestStep):
            return o.__dict__ == self.__dict__
        return False
    
    def to_code(self):
        def to_code_prefix(prefix):
            code = '' + prefix + '{ '
            for child in self.child:
                code += child.to_code() + '\n'
            return code + '}'

        def to_code_prefix_input(prefix):
            code = '' + prefix + self.input[0].to_code() + '{ '
            for child in self.child:
                code += child.to_code() + '\n'
            return code + '}'

        def to_code_normal():
            code = ''
            if self.receiver:
                code += self.receiver + '.'
                # print(self.receiver)
            code += self.action + '('
            if len(self.input) != 0:
                for arg in self.input:
                    code += arg.to_code() + ','
                code = code[:-1]
            code += ')'
            return code 

        if self.action == 'Assignment':
            lhs = [term.to_code() for term in self.output]
            rhs = [term.to_code() for term in self.input]
            return ','.join(lhs) + ' = ' + ','.join(rhs)
        elif self.action in ['Else', 'Try', 'Catch']:
            return to_code_prefix(self.action.lower())
        elif self.action in ['If', 'For', 'While']:
            return to_code_prefix_input(self.action.lower())
        else: 
            return to_code_normal()
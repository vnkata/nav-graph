from cProfile import label
from TestStep import TestStep
from snakes.nets import *
snakes.plugins.load('gv', 'snakes.nets', 'nets')
from nets import *
from typing import Tuple
import pickle
import re

from PathTraversal import RandomTraversal
from StateParser import StateParser
from CodeConverter import ImportIndex
from Graph import Graph
from State import MasterState
from .. import config

from loguru import logger

PLACE_POSTFIX = '_p'
FIND_ITEM_REGEX = re.compile(r"this.findTestObject\(.*\/([^\)]*)'\)")

class CustomPetriNet:
    init_state = MasterState()
    def __init__(self, name = "my-net", traverser = RandomTraversal, merge_cond = "action+assertion"):
        # id for test cases
        self.next_action_id = 0
        self.next_id = 0
        self.net = PetriNet(name)
        self.net.add_place(Place('initial-place'))

        # This help traverser the graph to create new test cases
        self.traverser = traverser

        # This contain list of imported library for each test case
        self.import_index = ImportIndex()

        # Save existing paths merged into the net
        self.old_path = []
    
        #place dict -> avoid self-looping
        self.place_cnt = {}
        self.cnt = 0
        self.mergeCond = merge_cond
        logger.info(f"Merge conditions for place: {merge_cond}")

    def insert_a_testcase(self, input_path: str) -> None:
        self.place_cnt.clear() #restarting place count
        sub_graph = StateParser.parse_a_testcase(input_path)
        self.merge(sub_graph)
        self.next_id += 1

        # input path: GroovyParser/Output/*.txt
        # corresponding script: GroovyParser/Data/*.groovy
        original_script = input_path.replace('Output', 'Data') \
                                    .replace('.txt', '.groovy')

        # print(original_script, script_path)
        self.import_index.read_import(original_script)

    # def merge(self, sub_graph: 'Graph') -> None:
    #     last_place = None # type: Place
    #     for graph_state in sub_graph.vertex.keys():
    #         transition, place = self.convert_graph_state_to_petrinet_component(graph_state)
            
    #         # Case for initial state
    #         if transition is None:
    #             last_place = place
    #             continue
                
    #         self.net.add_place(place)
    #         self.net.add_transition(transition)
    #         if last_place is not None:
    #             self.net.add_input(last_place.name, transition.name, Variable('o'))
    #         self.net.add_output(place.name, transition.name, Variable('o'))
                            
    #         last_place = place

    def write_original(self, trans, maxc):
        def get_cnt(maxc):
            res = str(self.cnt)
            while len(res) < len(str(maxc)): #padding for better look
                res = "0" + res
            self.cnt +=1 
            return res

        with open(config.FTEST_DIR + "Original/" + get_cnt(maxc) + ".txt","w",encoding="utf8") as f:
            f.write("\n".join(trans))


    def merge(self, sub_graph: Graph) -> None:
        trans_dict = []
        # print('START MERGING')
        for graph_state in sub_graph.vertex.keys():
            # print('[merge]', graph_state.cur_action, graph_state.prev_action, graph_state.tag)
            _, place = self.convert_graph_state_to_petrinet_component(graph_state,True)
            self.net.add_place(place)
            #print("P", place.name)

        self.place_cnt.clear()

        vertex_list = dict((v, k) for k, v in sub_graph.vertex.items())
        for u in range(len(sub_graph.edges)):
            for v in sub_graph.edges[u]:
                _, u_place = self.convert_graph_state_to_petrinet_component(vertex_list[u],False)
                transition, v_place = self.convert_graph_state_to_petrinet_component(vertex_list[v],True)
                #print("U", u_place,flush=True)
                #print("V", v_place,flush=True)
                transition.name = u_place.name + ";;;" + transition.name + ";;;" + v_place.name
                self.net.add_transition(transition)
                self.net.add_input(u_place.name, transition.name,  Variable('o'))
                self.net.add_output(v_place.name, transition.name,  Variable('o'))

                trans_dict.append(transition.name)
        
        self.write_original(trans_dict,100)
        
    def create_place_name(self, content, uorv) -> str:
        '''
            Merge condition for place merging. Return a string representation for a place
            2 places will be merged if their string representation are the same.
            Follow the snake framework
            @content --> type: Tuple[TestStep, List[TestStep]]
        '''
        action, assertions = content
        if action == '':
            return 'initial-place'
        # if assertions == []:
        #     name = action.to_code() + '_p'
        #     if name in self.place_cnt.keys(): #exists
        #         if uorv:
        #             self.place_cnt[name] += 1
        #     else: #not exists
        #         self.place_cnt.update({name:1})
        #     return name + str(int(self.place_cnt[name]))
        #     #return ''
        # else:
        #     name = ';'.join([assertion.to_code() for assertion in assertions]) + '_p'
        #     if name in self.place_cnt.keys(): #exists
        #         if uorv:
        #             self.place_cnt[name] += 1
        #     else: #not exists
        #         self.place_cnt.update({name:1})
        #     return name + str(int(self.place_cnt[name]))
        #action + assert
        if self.mergeCond == "action+assertion":
            name = action.to_code() + ";:;" + ';'.join([assertion.to_code() for assertion in assertions]) +";:;" +'_p' 
        #only action
        elif self.mergeCond == "action":
            name = action.to_code() + ";:;" + ";:;" +'_p'
        #only assert
        elif self.mergeCond == "assertion":
            if assertions == []:
                name = str(self.cnt) + ";:;" + ';'.join([assertion.to_code() for assertion in assertions]) +";:;" +'_p' 
            else:
                name = ";:;" + ';'.join([assertion.to_code() for assertion in assertions]) +";:;" +'_p'

        if name in self.place_cnt.keys(): #exists
            if uorv:
                self.place_cnt[name] += 1
        else: #not exists
            self.place_cnt.update({name:1})
        return name + str(int(self.place_cnt[name]))
        # return action.to_code() + '_p' + ';' + ';'.join([assertion.to_code() for assertion in assertions]) 

    def create_transition_name(self, action: TestStep) -> str:
        '''
            Merge condition for transition merging. Return a string representation for a transition
            2 transitions will be merged if their string representation are the same.
            Follow the snake framework
        '''
        # return action.to_code() 
        self.next_action_id += 1
        return action.to_code()# + str(self.next_action_id)

    def convert_graph_state_to_petrinet_component(self, graph_state: 'MasterState',uorv) -> Tuple[Transition, Place]:

        # Case initial state of the graph
        if graph_state == CustomPetriNet.init_state: 
            return (None, Place('initial-place'))

        # MasterState.cur_action type: TestStep
        action = ''
        if graph_state.cur_action is not None:
            action = graph_state.cur_action
            transition = Transition(self.create_transition_name(action))
            setattr(transition, "step_info", action)
        else:
            transition = None
        assertions = graph_state.assertions
        # assertions_str = ','.join([assertion.to_code() for assertion in assertions])
        # place = Place(action + assertions_str + PLACE_POSTFIX, set(assertions), self.next_id)
        # assertions = graph_state.assertions
        place = Place(self.create_place_name((action, assertions),uorv), set(assertions), self.next_id)
        return transition, place

    def render(self, output_name = 'Visualization/PetriNet.jpg') -> None:
        def draw_transition(trans, attr):
            # TODO: Minimize the name for readability
            if str(trans.guard) == "True":
                displayName = trans.name.split(";;;")
                # print(displayName[1])
                attr['label'] = self.reduce_name(displayName[1])
                # print(attr['label'])
            else:
                attr['label'] = f'{trans.name}\n{trans.guard}'

        def draw_place(place, attr):
            # attr['label'] = self.reduce_name(place.name)
            attr['label'] = ''
            # attr['style'] = 'filled'
            # pass

        def draw_arc(arc, attr):
            attr['label'] = ''

        self.net.draw(output_name, 
                        trans_attr=draw_transition, 
                        place_attr=draw_place,
                        arc_attr=draw_arc, engine='dot')

    def save(self, output_name = 'PetriNet.pkl') -> None:
        with open(output_name, 'wb+') as file:
            pickle.dump(self.net, file)

    def reduce_name(self, name):
        name = re.sub('WebUI.', '', name)
        action_target = re.search(FIND_ITEM_REGEX, name)
        if action_target is not None:
            action_target = action_target.group(1)
            reduced_name = str(re.sub(FIND_ITEM_REGEX, action_target, name))
            return reduced_name
        return name

    def summary(self):
        print('Number of transition merged', self.net.merge_action_cnt)
        print('Number of place merged', self.net.merge_place_cnt)
        

# name = "WebUI.click(this.findTestObject('11-Settings/Team Setup/mat-icon_search_TeamSetup'), FailureHandling.STOP_ON_FAILURE)"
# action_target = re.search(FIND_ITEM_REGEX, name).group(1)
# reduced_name = re.sub(FIND_ITEM_REGEX, action_target, name)
# print(reduced_name)
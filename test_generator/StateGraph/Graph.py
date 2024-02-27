import random
import pickle
from Util import CycleChecker
from Visualizer import Visualizer
from CodeConverter import CodeConverter, ImportIndex
from State import MasterState
from PathTraversal import RandomTraversal

class Graph:
    def __init__(self, initial_state=MasterState(), traverser=RandomTraversal()) -> None:
        # Vertex is stored in a dictionary with key: state, value: index
        # Edge is a list of tuple (x, y) indicates that there is a edge from state x to state y
        self.vertex = {initial_state: 0}
        self.edges = [[]]
        self.next_id = 1
        self.traverser = traverser
        self.old_path = []
        self.next_test_id = 0
        self.import_index = ImportIndex()

    def insert_a_testcase(self, script_path):
        from StateParser import StateParser
        sub_graph = StateParser.parse_a_testcase(script_path)
        original_script = script_path
        original_script = original_script.replace('Output', 'Data')
        original_script = original_script.replace('.txt', '.groovy')
        # print(original_script, script_path)
        self.import_index.read_import(original_script)
        self.merge(sub_graph)

    def insert(self, vertex_pair):
        src, dest = vertex_pair
        if src is None or dest is None:
            return
        if not (src in self.vertex):
            self.vertex[src] = self.next_id
            self.edges.append([])
            self.next_id += 1
            
        if not (dest in self.vertex):
            self.vertex[dest] = self.next_id
            self.edges.append([])
            self.next_id += 1
        
        src_id, dest_id = self.vertex[src], self.vertex[dest]
        if dest_id not in self.edges[src_id]:
            self.edges[src_id].append(dest_id)

    def insert_to_subgraph(self, vertex_pair):
        '''
            This version allow duplicated vertex
        '''
        src, dest = vertex_pair
        if src is None or dest is None:
            return
        
        vertices = list(self.vertex.keys())[::-1]
        if src in self.vertex:
            # Find the latest version set that version to src
            for vertex in vertices:
                if vertex.similar(src):
                    src.version_id = vertex.version_id
                    break

        # self.vertex[src] = self.next_id
        # self.edges.append([])
        # self.next_id += 1

        if dest in self.vertex:
            for vertex in vertices:
                if vertex.similar(dest):
                    dest.version_id = vertex.version_id + 1
                    break

        # print(src.get_description(), dest.get_description())
        self.vertex[dest] = self.next_id
        self.edges.append([])
        self.next_id += 1
        
        src_id, dest_id = self.vertex[src], self.vertex[dest]
        if dest_id not in self.edges[src_id]:
            self.edges[src_id].append(dest_id)

    def merge(self, sub_graph: 'Graph') -> None:
        v_list = list(sub_graph.vertex.keys())
        for u in range(len(sub_graph.edges)):
            for v in sub_graph.edges[u]:
                v_list[u].test_id.add(self.next_test_id)
                v_list[v].test_id.add(self.next_test_id)
                self.insert((v_list[u], v_list[v]))

        v_list = [self.vertex[v] for v in v_list]
        self.old_path.append(v_list)
        self.next_test_id += 1

    def summary(self, name='out.html'):
        # print("Graph constructed")
        # print(len(self.vertex.keys()))
        # # for v in self.vertex.keys():
        # #     print(v, self.vertex[v], v.__hash__())
        # print(self.edges)
        # print("Checking for cycles ...")
        # cycle_checker = CycleChecker(self.vertex, self.edges)
        # cycle_checker.SCC()
        # print("=" * 80)
        self.visualizer = Visualizer(self.vertex, self.edges)
        self.visualizer.show(name)
           
    def generate(self):
        all_paths = self.traverser.generate(self.edges)
        # print("All paths", all_paths)
        # print("Old paths", self.old_path)
        # new_paths = all_paths
        new_paths = [path for path in all_paths if path not in self.old_path]
        v_list = list(self.vertex.keys())
        for i, path in enumerate(new_paths):
            path = [v_list[v] for v in path]
            with open(f'Output/Testcase{i}.groovy', 'w+') as file:
                file.write(self.import_index.get_imports(path))
                file.write(CodeConverter.convert(path))
        return new_paths

    def save(self):
        with open("Graph.pkl", 'wb+') as file:
            pickle.dump(self, file)
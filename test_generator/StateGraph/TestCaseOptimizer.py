from unicodedata import name
from .PetriNet import CustomPetriNet
from .Graph import Graph
from .Visualizer import Visualizer
from snakes.nets import Place, PetriNet

from typing import Union, Dict, List

class Edge:
    def __init__(self, u, v, action) -> None:
        self.action = action
        self.u, self.v = u, v


class OptimizeGraph:
    def __init__(self, presentation: Union[CustomPetriNet, Graph]) -> None:
        self.next_id = 0
        self.vertex = [] # type : List[int]
        self.edges = [] # Adjacency matrix, type: List[List[Edge]] 
        self.invert_vertex_index = {} # type: Dict[Place, int]
        if isinstance(presentation, CustomPetriNet):    
            self.from_petri_net(presentation.net)
        else:
            pass

        self.V = len(self.vertex)
        self.Time = 0 # type: int

    def from_petri_net(self, presentation: PetriNet):
        for place in presentation.place():
            self.vertex.append(place)
            self.invert_vertex_index[place] = self.next_id
            self.next_id += 1

        self.edges = [[] for _ in range(self.next_id)] # Adjacency matrix, type: List[List[Edge]] 

        for transition in presentation.transition():
            name = transition.name
            input, output = transition.input(), transition.output()
            for i in input:
                for o in output:
                    in_place, _ = i
                    out_place, _ = o
                    assert in_place in self.invert_vertex_index, 'Unknown input place'
                    assert out_place in self.invert_vertex_index, 'Unknown output place'
                    in_index = self.invert_vertex_index[in_place]
                    out_index = self.invert_vertex_index[out_place]

                    self.edges[in_index].append(Edge(in_index, out_index, name))
    
    def SCCUtil(self,u, low, disc, stackMember, st):
        # Initialize discovery time and low value
        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1
        stackMember[u] = True
        st.append(u)
 
        # Go through all vertices adjacent to this
        for e in self.edges[u]:
            v = e.v
            # If v is not visited yet, then recur for it
            if disc[v] == -1 :
             
                self.SCCUtil(v, low, disc, stackMember, st)
 
                # Check if the subtree rooted with v has a connection to
                # one of the ancestors of u
                # Case 1 (per above discussion on Disc and Low value)
                low[u] = min(low[u], low[v])
                         
            elif stackMember[v] == True:
 
                '''Update low value of 'u' only if 'v' is still in stack
                (i.e. it's a back edge, not cross edge).
                Case 2 (per above discussion on Disc and Low value) '''
                low[u] = min(low[u], disc[v])
 
        # head node found, pop the stack and print an SCC
        w = -1 #To store stack extracted vertices
        if low[u] == disc[u]:
            scc = []
            while w != u:
                w = st.pop()
                scc.append(w)
                stackMember[w] = False
            if len(scc) != 1:
                self.scc.append(scc) 

    # The function do DFS traversal.
    # It uses recursive SCCUtil()
    def detect_cycle(self):
        """
            Find strong connected component using Tarjan algorithm
            return the list of strong connected component in self.scc
        """
        self.scc = []
        self.Time = 0
        disc = [-1] * (self.V)
        low = [-1] * (self.V)
        stackMember = [False] * (self.V)
        st = []

        for i in range(self.V):
            if disc[i] == -1:
                self.SCCUtil(i, low, disc, stackMember, st)

    def create_sub_graph(self, nodes: List[Place]) -> 'OptimizeGraph':
        '''
            Create subgraph from a list of nodes
        '''
        subgraph = OptimizeGraph()
        for node in nodes:
            pass

    def remove_cycle(self):
        '''
            Replace a cycle in the graph with a representative node
        '''
        


    def create_flow_graph(self):
        pass

    def summary(self):
        print("Hello")
        print(self.scc)
        self.visualizer = Visualizer(self.invert_vertex_index, [[e.v for e in subitem] for subitem in self.edges])
        self.visualizer.show('Optimize graph.html')        

class TestCaseOptimizer:
    def __init__(self, presentation):
        self.net = OptimizeGraph(presentation)
    
    def optimize(self):
        self.net.detect_cycle()
        self.net.summary()
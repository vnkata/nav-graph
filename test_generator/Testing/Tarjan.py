from queue import Queue
  
INF = 1000

class Graph:
  
    def __init__(self, vertices, edges):
        self.V= len(vertices)
        self.vertices = vertices
        self.graph = edges        
        self.scc = [] 
        self.removed = [False] * self.V
       
    def SCCUtil(self,u, low, disc, stackMember, st):
        # Initialize discovery time and low value
        disc[u] = self.Time
        low[u] = self.Time
        self.Time += 1
        stackMember[u] = True
        st.append(u)
 
        # Go through all vertices adjacent to this
        for v in self.graph[u]:
             
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
    # The function to do DFS traversal.
    # It uses recursive SCCUtil()
    def SCC(self):
        """
            Find strong connected component using Tarjan algorithm
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

    def uncycle(self):
        
        for scc in self.scc:
            # Create new node
            self.graph.append([])
            self.removed.append(False)
            self.V += 1
            s = set()

            # Create outgoing edge, remove all outgoing edge of cycles
            for u in scc:
                s.update(self.graph[u])
                self.graph[u] = []
                self.removed[u] = True
            s = s.difference(set(scc))
            self.graph[-1] = list(s)

            # Create incomming edge
            for i in range(len(self.graph)):
                # Skip node not in scc
                if i in scc:
                    continue

                found = False

                # For in reverse order
                for j in range(len(self.graph[i]) - 1, -1, -1):                   
                    if self.graph[i][j] in scc:
                        self.graph[i].remove(self.graph[i][j])
                        found = True
                if found:
                    self.graph[i].append(self.V - 1)

    def generate_flow_graph(self):
        inverted_index = {}
        vertices, edges = self.get_vertices_edge()
        for u, v in zip(vertices, range(len(vertices))):
            inverted_index[u] = v
        
        vertices = [inverted_index[i] for i in vertices]
        edges = [[inverted_index[i] for i in conn] for conn in edges]

        flow_graph = Graph(vertices=vertices, edges=edges)
        s, t = flow_graph.get_start_sink()
        print(s, t)
        for v in range(flow_graph.V):   
            if v == s or v == t:
                self.graph[v] = [(x, 0, INF, 0) for x in self.graph[v]]
                continue

            flow_graph.vertices += [flow_graph.V, flow_graph.V + 1]
            for _ in range(2):
                flow_graph.graph.append([])
                flow_graph.removed.append(False)
            flow_graph.V += 2

            # Outcoming edges
            flow_graph.removed[v] = True
            flow_graph.graph[-1] = [(x, 0, INF, 0) for x in flow_graph.graph[v]]

            # Incoming edges
            for u in range(flow_graph.V):
                for i, _ in enumerate(flow_graph.graph[u]):
                    if flow_graph.graph[u][i] == v:
                       flow_graph.graph[u][i] = (flow_graph.V - 2, 0, INF, 0)
                       
            flow_graph.graph[-2].append((flow_graph.V - 1, 1, INF, 0))


        assert len(flow_graph.vertices) == len(flow_graph.graph)
        return flow_graph

    def assign_feasible_flow(self):
        s, t = self.get_start_sink()
        for v in self.vertices:
            if not self.removed[v] and v not in (s, t):
                p_s = self.bfs(s, v)
                p_t = self.bfs(v, t)
                s = p_s + p_t

                k = 0
                for u, v in s:
                    for v_, l, _, f in self.graph[u]:
                        if v == v_:
                            k = min(k, f - l)
                
                if k < 0:
                    for u, v in s:
                        for e in self.graph[u]:
                            if v == e[0]:
                                e[-1] += 1
                                break
                                
    def bfs(self, src, dest):
        pred = [-1] * len(self.vertices)
        
        queue = Queue()

        queue.put(src)
        pred[src] = src

        while not queue.empty():
            u = queue.get()
            
            if u == dest:
                break
            
            # print(f"Debug: {u}, {self.graph[u]}")
            # print(self.vertices)
            for v, _, _, _ in self.graph[u]:
                id = self.vertices.index(v)
                if pred[id] != -1:
                    queue.put(v)
                    pred[id] = u
            
        path = []
        while pred[dest] != dest:
            path.append(dest)
            dest = pred[dest]
        path.append(src)
        return path[::-1]

            

    def get_start_sink(self):
        start = 0
        sink = -1
        for u in range(len(self.vertices)):
            if not self.removed[u] and self.graph[u] == []:
                sink = u
                return start, sink

    def get_vertices_edge(self):
        vertices = [i for i in range(self.V) if not self.removed[i]]
        edges = [self.graph[i] for i in range(self.V) if not self.removed[i]]
        return vertices, edges

    def summary(self):
        print("============================SUMMARY===========================")
        print(len(self.removed), self.V)
        print([i for i in range(self.V) if not self.removed[i]])
        print([self.graph[i] for i in range(self.V) if not self.removed[i]])
        u, v = self.get_start_sink()
        print(f'Start node: {u}, sink node: {v}')
        print("==============================================================")


g = Graph([0, 1, 2, 3, 4, 5, 6, 7, 8], [[1, 4], [2], [3], [1, 7], [1, 2, 5], [6], [5, 8], [2, 8], []])
g.SCC()
print(g.scc)
g.summary()
g.uncycle()
g.summary()
flow = g.generate_flow_graph()

flow.summary()
# print(flow.bfs(0, 8))
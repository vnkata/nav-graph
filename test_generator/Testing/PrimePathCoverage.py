class Graph:
  
    def __init__(self, vertices, edges):
        self.V = len(vertices)
        self.vertices = vertices
        self.edges = edges        

    def getAllEdge(self):
        res = []
        for u in range(self.vertices):
            for v in self.edges[u]:
                res.append(Graph([u, v], [[v]]))
        return res 

    def add_edge(self, u, v):
        if v not in self.vertices:
            self.vertices.append(v)
            self.edges.append([])
        
        self.edges[u].append(v)

    def getAllPrimePaths(self):
        """
            No longer need
        """

        p_prime = [[i] for i in range(self.V)]
        explored = set()

        while True:
            finished = True

            for i, p in enumerate(p_prime):
                extended = False
                if tuple(p) in explored:
                    continue
                if p[0] != p[-1] or len(p) == 1:
                    u = p[-1]
                    for v in self.edges[u]:
                        if v not in p or v == p[0]:
                            p_prime.append(p + [v])
                            finished = False
                            extended = True
                        else:
                            explored.add(tuple(p))
                if extended:
                    p_prime.remove(p)

            if finished:
                break
        
        paths = list(p_prime)[::-1]
        return paths
    
    
            

g = Graph(list(range(7)), [[1], [2, 3], [6], [4], [1, 5], [4], []])
print(g.getAllPrimePaths())

                        
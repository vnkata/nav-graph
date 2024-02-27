class GraphTraversal:
    def choose_next_vertex(self):
        pass
    def generate(self, edge, start_node=[0]):
        pass

class RandomTraversal(GraphTraversal):
    def __init__(self, max_paths = 25) -> None:
        super().__init__()
        self.MAX_PATHS = max_paths

    def count_path(self, edge):
        """
            This function checks number of path generated from graph
        """
        # TODO: Topological sort, and use dp for calculation (in case there is no loop in the graph)
        

    def generate(self, edge, start_node=0):
        """
            This function return all paths generated from graph
        """
        # assert self.count_path() <= 100, "Too many path could be generated"
            
        all_path = []
        current_path = [start_node]

        def dfs_helper(node):
            nonlocal all_path, current_path
            if len(all_path) >= self.MAX_PATHS:
                return
                
            if len(edge[node]) == 0:
                all_path.append(current_path.copy())
                

            for candidate_id in edge[node]:
                if not candidate_id in current_path:
                    current_path.append(candidate_id)       
                    dfs_helper(candidate_id) 
                    current_path.pop()
            
        dfs_helper(start_node)
        return all_path

class Edge:
    def __init__(self, cur_index, prev_index=0, condition=None) -> None:
        self.cur_index = cur_index
        self.prev_index = prev_index
        self.condition = condition
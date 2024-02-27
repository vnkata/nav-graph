from StateGraph.Graph import Graph
import copy

class FrequentItemset:
    def __init__(self) -> None:
        self.graphs = []
        self.flat_graphs = []
        self.freq_list = []
        self.single_freq_list = []
        self.chosen_list = []

    def add_graph(self, g):
        next_id = 1
        flat_graph = []
        self.graphs.append(copy.deepcopy(g))
        while g.edges[next_id] is not None:
            flat_graph.append(g.vertex[next_id])
            #assuming edges[next_id] only has one element
            next_id = g.edges[next_id][0]
        
        self.flat_graphs.append(flat_graph)


    def find_freqitem(self):
        
        #inner func
        def add_Freqlist(pair):
            for idx in range(len(self.freq_list)):
                if self.freq_list[idx][0] == pair:
                    self.freq_list[idx][1] += 1
                    return

            self.freq_list.append(tuple( (pair,1) ))

        def add_SingleFreqlist(item):
            for idx in range(len(self.single_freq_list)):
                if self.single_freq_list[idx][0] == item:
                    self.single_freq_list[idx][1] += 1
                    return

            self.freq_list.append(tuple( (item,1) ))

        # count frequent single item
        for flat in self.flat_graphs:
            for step in flat:
                add_SingleFreqlist(step)

        # count frequent pair item
        for flat in self.flat_graphs:
            tmp_pair = []
            for i in range(1,len(flat)):
                tmp_pair = tuple( (flat[i],flat[i-1]) )

                add_Freqlist(tmp_pair)
                tmp_pair = []


    # zero one of the variable to ignore it
    # freqThreshold ranges [0, +inf), confidenceLevel ranges [0,1]
    def filter(self, freqThreshold = 5, confidenceLevel = 0.5):

        def cal_freq(target, pairFreq):
            for item in self.single_freq_list:
                if item[0] == target:
                    return pairFreq/item[1]

        # choose frequent item
        for item in self.freq_list:
            if item[1] >= self.threshold and cal_freq(item[0][0], item[1]) > confidenceLevel:
                self.chosen_list.append(item[0])


    def take_graphs(self):
        # filter graphs
        for g in self.graphs:
            next_id = 1
            elect_pair = []
            while g.edges[next_id] is not None:
                tmp_nextid = g.edges[next_id][0]
                elect_pair.append( (g.vertex[next_id],g.vertex[tmp_nextid]) )
                if tmp_nextid == None:
                    continue

                if elect_pair in self.chosen_list:
                    g.vertex[next_id].child_state.append(g.vertex[tmp_nextid].cur_action)
                    g.vertex[next_id].assertions += g.vertex[tmp_nextid].assertions
                    g.edges[next_id][0] = g.edges[tmp_nextid][0]
        
                next_id = g.edges[next_id][0]
                elect_pair = []

        # return graph
        return self.graphs



        

    
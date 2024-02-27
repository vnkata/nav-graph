import pickle
import re
from typing import List, Set, TypeVar, Union
from comparators.cmp_place import LessStrictPlaceComparator
from repository.core import ObjectManager
from utils import randomword


class Arc(object):
    """
    This class defines an arc from a place to a transition, or a transition to a place in a Petri net.
    """

    def __init__(self, source, destination, weight=0, data=None) -> None:
        src_type = source.get_node_type()
        dest_type = destination.get_node_type()
        # !(Logical XOR)
        if (src_type in ["Place", "Page"] and dest_type in ["Transition"]) == (dest_type in ["Place", "Page"] and src_type in ["Transition"]):
            raise Exception(
                "Petri net arcs must connect from places/pages to transitions or vice versa.")
        self.__src = source
        self.__dest = destination
        self.__weight = weight
        self.__data = data

    @property
    def source(self):
        return self.__src

    @property
    def destination(self):
        return self.__dest

    @property
    def weight(self):
        return self.__weight

    @property
    def data(self):
        return self.__data

    def __repr__(self) -> str:
        src_repr = repr(self.__src)
        dest_repr = repr(self.__dest)
        rep = src_repr  # + "-"
        # if self.data is not None:
        #     rep += f"({self.data})"
        rep += " -> " + dest_repr
        return rep

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other) -> bool:
        return self.source == other.source and self.destination == other.destination


class Node(object):
    """
    This class defines a node of any type in the Petri net.
    It should be inherited by the place, transition or page node.
    """

    def __init__(self, name, data=None) -> None:
        self.__name: str = name
        self.__data: Union[str, dict, list] = data
        self.__input_arcs: dict = {}
        self.__output_arcs: dict = {}

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, new_data):
        self.__data = new_data

    def get_node_type(self):
        return "Undefined"

    def input_arc(self, src_name=None):
        if src_name is None:
            return self.__input_arcs.values()
        return self.__input_arcs.get(src_name, None)

    def output_arc(self, dest_name=None):
        if dest_name is None:
            return self.__output_arcs.values()
        return self.__output_arcs.get(dest_name, None)

    def __repr__(self) -> str:
        return f"{self.get_node_type()}_{self.name}"

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other) -> bool:
        return self.get_node_type() == other.get_node_type() and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def add_input_arc(self, arc: Arc):
        if arc.destination != self:
            raise Exception(
                f"The input arc ({str(arc)}) for node {self.name} should point to this node.")
        self.__input_arcs[arc.source.name] = arc

    def add_output_arc(self, arc: Arc):
        if arc.source != self:
            raise Exception(
                f"The output arc ({str(arc)}) for node {self.name} should go from this node.")
        self.__output_arcs[arc.destination.name] = arc

    def add_input_node(self, node, weight=0, data=None):
        new_arc = Arc(node, self, weight, data)
        self.add_input_arc(new_arc)

    def add_output_node(self, node, weight=0, data=None):
        new_arc = Arc(self, node, weight, data)
        self.add_output_arc(new_arc)

    def remove_input_node(self, node_name):
        if node_name is not None:
            self.__input_arcs.pop(node_name, None)

    def remove_output_node(self, node_name):
        if node_name is not None:
            self.__output_arcs.pop(node_name, None)


class Place(Node):
    """
    This class represents a place node within the petri net.
    A place contains the elements defining a webpage and (optionally) the assertions about said elements.
    """

    def __init__(self, name, data=None) -> None:
        super().__init__(name, data)
        self.__page_elements = []
        # TODO: Add the assertion list attribute to this class

    @property
    def page_elements(self):
        return self.__page_elements

    # Override
    def get_node_type(self):
        return "Place"

    def __repr__(self) -> str:
        # don't include any special character in the returned value, 
        # it will affect the visualizer
        return f"{self.name}"


class Page(Node):
    """
    This class represents a Page node within the petri net.
    A Page contains the list of places in the petri net similar to each other.
    It functions similarly to the place node and has to be connected to the transition node.
    """

    def __init__(self, name, data=None) -> None:
        super().__init__(name, data)
        self.__place_list = []

    def add_place(self, place: Place) -> None:
        self.__place_list.append(place)

    @property
    def place_list(self):
        return self.__place_list

    # Override
    def get_node_type(self):
        return "Page"


class Transition(Node):
    """
    This class represents a transition node within the petri net.
    A transition contains the element causing the webpage transition.
    This is just a simple class to hold the data and the info of the actionable element.
    """

    def __init__(self, name, node_data=None) -> None:
        super().__init__(name, node_data)
        self.__history: dict[str, list[str]] = {}
        #self._element_id = element_id
        # self._transition_data = transition_data

    @property
    def history(self) -> dict:
        return self.__history

    def add_history(self, from_name, to_name):
        if self.__history.get(from_name, None) is None:
            self.__history[from_name] = [to_name]
        else:
            self.__history[from_name].append(to_name)

    def get_history_from(self, from_name):
        if self.__history.get(from_name, None) is None:
            return None
        else:
            return self.__history[from_name][0]

    def get_history_list_from(self, from_name):
        return self.__history.get(from_name, None)

    # Override
    def get_node_type(self):
        return "Transition"

    # @property
    # def element_id(self):
    #     return self._element_id

    # @property
    # def transition_data(self):
    #     return self._transition_data


class ActionableTransition(Transition):
    """
    This class defines the specific action that causes a page transition.
    """

    def __init__(self, name, node_data=None, transition_type="actionable") -> None:
        super().__init__(name, node_data)
        self._transition_type = transition_type

    @property
    def transition_type(self):
        return self._transition_type

    def is_similar(self, other) -> bool:
        return self.data == other.data and self.transition_type == other.transition_type

    def __repr__(self) -> str:
        if self.data is not None:
            tag = self.data.get_attribute("tag_name")
            accesible_name = self.data.get_attribute("accessible_name")
            return f"\"{self.name}__{self.transition_type}__{tag}__{accesible_name}\""
        else:
            return f"\"{self.name}__{self.transition_type}\""
  
Petrinet = TypeVar("Petrinet", bound="PetriNet")  
class PetriNet(object):
    """
    This class represents a petri net generated in the webpage crawling process.
    """

    def __init__(self, root_node: Union[Place, Page] = None) -> None:
        """
        Create a Petri Net from a root node. If root node is not specified, the petri net is empty.
        The includeChild argument has the same use as the one in PetriNet.add_node() method.

        Parameters
        ----------
        root_node : Union[Place, Page], optional
            The root node of the petri net, must be either a Page or a place node, by default None
        includeChild : bool, optional
            A flag determining whether or not all the connections to the root node should be included in the petri net or stripped, by default False

        Raises
        ------
        Exception
            The petri net root is not a Page or Place node
        """
        self.__places: dict[str, Place] = {}
        self.__transitions: dict[str, Transition] = {}
        self.__pages: dict[str, Page] = {}
        self.__nodes = {}
        self.__dict_switch = {
            "Place": self.__places,
            "Transition": self.__transitions,
            "Page": self.__pages
        }
        # Add root node to the petri net
        self.__root = []
        if root_node is not None:
            self.root.append(root_node)

    @property
    def root(self):
        return self.__root

    def add_root(self, node: Union[Place, Page]):
        if node.get_node_type() not in ["Place", "Page"]:
            raise Exception("The root must be a place or a page.")
        self.root.append(node)
        self.add_node(node, True)

    def node(self, node_name=None):
        if node_name is None:
            return self.__nodes.values()
        return self.__nodes.get(node_name, None)

    def place(self, node_name=None):
        if node_name is None:
            return self.__places.values()
        return self.__places.get(node_name, None)

    def transition(self, node_name=None):
        if node_name is None:
            return self.__transitions.values()
        return self.__transitions.get(node_name, None)

    def page(self, node_name=None):
        if node_name is None:
            return self.__pages.values()
        return self.__pages.get(node_name, None)

    def add_node(self, new_node: Node, includeChild=True):
        """
        Add a node to the petri net. The node can be initialized beforehand with arcs included before being added.
        If the node already has arcs connected to it, this method will also recursively add the connected nodes to the petri net if the includeChild flag is toggled. Otherwise, if the flag isn't triggered, any connection outside of the current petri net will be stripped.
        If the petri net initially doesn't have a root, set the root as the added node.
        
        Parameters
        ----------
        new_node : Node
            The node to be added to this petri net
        includeChild : bool, optional
            The flag to determine whether or not the children of the added nodes will also be included, by default False
        """
        if self.node(new_node.name) is None:
            self.__dict_switch[new_node.get_node_type()
                               ][new_node.name] = new_node
            self.__nodes[new_node.name] = new_node
            if len(self.root) == 0 and new_node.get_node_type() in ["Place", "Page"]:
                self.root.append(new_node)
        else:
            return
        if includeChild:
            child_nodes = [arc.destination for arc in new_node.output_arc()]
            for node in child_nodes:
                self.add_node(node)
        else:
            child_nodes = [arc.destination for arc in new_node.output_arc()]
            for node in child_nodes:
                node_name = node.name
                if self.node(node_name) is None:
                    new_node.remove_output_node(node_name)
                
    def add_arc(self, source: Node, destination: Node, weight=0, data=None):
        if source.get_node_type() == "Undefined" or destination.get_node_type() == "Undefined":
            raise Exception(
                "Error: The source or destination node type is undefined.")
        # Check if the nodes exist in the petri net
        src: Node = self.__dict_switch[source.get_node_type()][source.name]
        dest: Node = self.__dict_switch[destination.get_node_type(
        )][destination.name]
        if src is None:
            self.add_node(source)
        if dest is None:
            self.add_node(destination)
        # Retrieve the nodes then add new arcs to them
        source.add_output_node(destination, weight, data)
        destination.add_input_node(source, weight, data)
        
    # def verify(self):
    #     """
    #     Petri Net must be complete and has 1 root, this method is for verifying such property.
    #     If there's a non-root node in the petri net which doesn't have any input arc, it's the root of another subgraph, and so the petri net is incomplete.
    #     """
    #     if self.root is None:
    #         raise Exception("Petri Net root is undefined.")
    #     for node in self.node():
    #         if node != self.root and (node.input_arc() is None or len(node.input_arc()) == 0):
    #             return False
    #     return True

    def merge_places(self, object_manager: ObjectManager):
        """
        Merge similar places into one page object.
        The places are not discarded, but rather clustered into a page.
        """
        def add_arc_to_page(page, place):
            """Helper to add in/out arcs of a place to its wrapping page."""
            for input_arc in place.input_arc():
                self.add_arc(input_arc.source, page)
            for output_arc in place.output_arc():
                self.add_arc(page, output_arc.destination)

        visited = set()
        places = list(self.place())
        for i in range(len(places)):
            if i in visited:
                continue
            visited.add(i)
            page = Page(randomword(5), data="")
            self.add_node(page)
            page.add_place(places[i])
            add_arc_to_page(page, places[i])

            for j in range(i+1, len(places)):
                if j in visited:
                    continue
                if LessStrictPlaceComparator(places[i], places[j], object_manager):
                    visited.add(j)
                    page.add_place(places[j])
                    add_arc_to_page(page, places[j])
            
    @classmethod
    def save(cls, petrinet, file_path):
        with open(file_path, "wb") as save_file:
            pickle.dump(petrinet, save_file)

    @classmethod
    def load(cls, file_path):
        with open(file_path, "rb") as load_file:
            return pickle.load(load_file)

    @staticmethod
    def merge(ptnBase: Petrinet, ptnTarget: Petrinet):
        """
        Merge target petri-net into the base petri-net based on the transition nodes. Return the merged instance of the base petri-net while also destroy the target petri-net.

        Parameters
        ----------
        ptnBase : PetriNet
            The base petri-net
        ptnTarget : PetriNet
            The petri-net to be merged into the base one
        """
        transSetA: Set[ActionableTransition] = set(ptnBase.transition())
        transSetB: Set[ActionableTransition] = set(ptnTarget.transition())
        for transA in transSetA:
            temp = transSetB.copy()
            for transB in temp:
                if transB.is_similar(transA):
                    # Bring input and output arcs from B to A
                    input_arcs: List[Arc] = transB.input_arc()
                    output_arcs: List[Arc] = transB.output_arc()
                    for arc in input_arcs:
                        arc.source.remove_output_node(transB.name)
                        arc.source.add_output_node(
                            transA, arc.weight, arc.data)
                        transA.add_input_node(arc.source, arc.weight, arc.data)
                    for arc in output_arcs:
                        arc.destination.remove_input_node(transB.name)
                        arc.destination.add_input_node(
                            transA, arc.weight, arc.data)
                        transA.add_output_node(
                            arc.destination, arc.weight, arc.data)
                    # Merge the history records
                    # transA.history.update(transB.history)
                    transSetB.remove(transB)
        # Add new independent transitions from petrinet B to A
        for transB in transSetB:
            ptnBase.add_node(transB)
        # Add all places from petrinet B to A
        for placeB in ptnTarget.place():
            ptnBase.add_node(placeB)
        # Add all roots from petrinet B to A
        ptnBase.root.extend(ptnTarget.root)
        return ptnBase
                    
    @staticmethod
    def SwallowMerge(ptnBase: Petrinet, ptnTarget: Petrinet):
        ptnBase.root.extend(ptnTarget.root)
        return ptnBase


class NavigationGraph(object):
    """
    A wrapper class represents a Navigation Graph generated in the webpage crawling process.
    The navigation graph consists of multiple subgraphs which are petri nets.
    ***(TODO: To be discussed) These petri nets can't contain Page nodes.
    """

    def __init__(self, name: str = None) -> None:
        self.__name = name if name is not None else "None"
        self.__subgraphs: List[PetriNet] = []
    
    
# class StateFlowGraph(object):
#     """
#     A wrapper class represents a State Flow Graph generated from the Navigation Graph when performing downstream tasks.
#     The state flow graph has a single petri net whose node types are just States and Transitions.
#     ***(TODO: To be discussed) The petri net can't contain Place nodes, only State nodes which are merged from Places.
#     """        
    
#     def __init__(self, name: str=None, petrinet: PetriNet=None) -> None:
#         self.__name = name if name is not None else "None"
#         self.__graph: PetriNet = None
#         if petrinet is not None:
#             if petrinet.place() is None:
#                 self.__graph = petrinet
#             else:
#                 raise Exception("State Flow Graph must merge places into states.")
#                 raise Exception("State Flow Graph must merge places into states.")

#  Created by nphau on 9/15/22, 11:52 PM
#  Copyright (c) 2022 . All rights reserved.
#  Last modified 9/15/22, 11:52 PM

import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from functools import partial
from typing import List
from comparators.cmp_place import LessStrictPlaceComparator
from repository.core import ObjectManager
from utils import standardize_value
from loguru import logger

import files
from petrinet.PetriNet import Place, Transition, PetriNet
from page.page import PageData

checked_nodes: list[str] = []

def get_node_style(current, selected=None, init_path=None):
    global checked_nodes
    if init_path is None:
        init_path = []
    if current in init_path:
        if current == selected:
            return {"color": "darkgreen",
                    "fillcolor": "darkgreen", "fontcolor": "white", "fontname": "Arial", "penwidth": 2}
        else:
            if current in checked_nodes:
                return {"color": "honeydew2",
                        "fillcolor": "honeydew2", "fontcolor": "black", "fontname": "Arial", "penwidth": 4}
            else:
                return {"color": "gray35",
                        "fillcolor": "gray95", "fontcolor": "black", "fontname": "Arial", "penwidth": 4}
    elif current == selected:
        return {"color": "darkgreen",
                "fillcolor": "darkgreen", "fontcolor": "white", "fontname": "Arial", "penwidth": 2}
    else:
        return {"color": "grey",
                "fillcolor": "white", "fontcolor": "black", "fontname": "Arial", "penwidth": 2}


# color
def get_transition_style(src, desc, init_path=None):
    if init_path is None:
        init_path = []
    if src in init_path and desc in init_path:
        return "darkgreen"
    return 'black'

def build_node(node: Place, selected, init_path=None):
    global checked_nodes
    if init_path is None:
        init_path = []
    node_name = node.name
    logger.debug(f"node.data={node.data}")
    if isinstance(node.data, dict):
        #title = "unknown...."
        title = node.data.get("title", "unknown")
    else:
        title = node.data.title or "untitled"
    label = standardize_value(title)
    visual_settings = get_node_style(node_name, selected, init_path)
    if getattr(node.data, 'from_test_script', False) == True:
        visual_settings['color'] = 'darkgoldenrod2'
        label = "<&nbsp;&nbsp;>"

    visual_style = " ".join([f"{k}={v}" for k, v in visual_settings.items()])
    if node_name == selected:
        ret = f"{node_name} [label={label} {visual_style}];\n"
        logger.info(f"node_name={node_name}, selected={selected} {ret}")
    return f"{node_name} [label={label} {visual_style.strip()}];\n"


def build_transition(transition, selected, init_path=None):
    global checked_nodes
    if init_path is None:
        init_path = []
    transition_name = transition.name
    tag_name = transition.data.json.get("tag_name", 'unknown')
    if tag_name == 'a': tag_name = 'link'

    action_type = transition.transition_type
    visible_text = transition.data.get_attribute('accessible_name')
    if visible_text is None:
        visible_text = transition.data.get_attribute('name')
    label = f"< {action_type}({tag_name}, {visible_text}) >"
    label = standardize_value(label)
    visual_settings = get_node_style(transition_name, selected, init_path)
    if transition.data.get_attribute('from_test_script', False) == True:
        visual_settings['color'] = 'darkgoldenrod2'

    visual_style = " ".join([f"{k}={v}" for k, v in visual_settings.items()])
    return f"{transition_name} [label={label} {visual_style}];\n"


def build_terminated_transition(transition: Transition):
    return f"{transition.name} [label=closeBrowser fillcolor=white style=dashed];\n"


def build_nodes(net: PetriNet, selected: str = None, init_path=None):
    if init_path is None:
        init_path = []
    lang = "node [shape=oval, style=filled];\n"
    for place in net.place():
        lang += build_node(place, selected, init_path)

    lang += "node [shape=box];"
    for transition in net.transition():
        if len(transition.output_arc()) == 0:
            lang += build_terminated_transition(transition)
            continue
        lang += build_transition(transition, selected, init_path)
    return lang


def build_arcs(net: PetriNet, init_path=None):
    if init_path is None:
        init_path = []
    lang = ""
    for node in net.node():
        for arc in node.output_arc():
            source = arc.source
            destination = arc.destination
            if source.get_node_type() == 'Page' or destination.get_node_type() == 'Page':
                continue

            if source is not None and destination is not None:
                color = get_transition_style(source.name, destination.name, init_path)
                lang += f"{source.name}->{destination.name} [color={color}]\n"
    return lang


def find_potential_connected_transitions(src: Place, invalid_place_names, other_nets, place_cmp) -> List[Transition]:
    for net_abc in other_nets:
        logger.info(f"****** Check net: {net_abc} to find similar P-T****")
        for p_abc in net_abc.place():
            if p_abc.name in invalid_place_names: continue
            p_next_transition: Transition = list(p_abc.output_arc())[0].destination
            if place_cmp(src, p_abc):
                yield p_next_transition


def build_graphviz(merged_net, all_nets, selected=None, init_path=None):
    def build_virtual_arcs(all_nets):
        xlang = ""
        objManager = ObjectManager("../running_logs")
        place_cmp = partial(LessStrictPlaceComparator, objManager=objManager)

        try:
            for selected_net in all_nets:
                other_nets = [x for x in all_nets if x != selected_net]
                invalid_place_names = [p.name for p in selected_net.place()]
                for pp in selected_net.place():
                    try:
                        for tr in find_potential_connected_transitions(pp, invalid_place_names, other_nets=other_nets,
                                                                       place_cmp=place_cmp):
                            # xlang += f"{pp.name}->{tr.name} [color=black style=dashed]\n"
                            pass
                    except Exception as e:
                        logger.info(e)
        except Exception as e:
            logger.debug(e)
        return xlang

    lang = "strict digraph G {"
    lang += build_nodes(merged_net, selected, init_path)
    lang += build_arcs(merged_net, init_path)

    if os.path.exists('virtual_arcs.txt'):
        with open('virtual_arcs.txt', 'r') as fp:
            virtual_arcs = fp.read()
    else:
        logger.error("Can not found virtual_arcs.txt file!")
        virtual_arcs = build_virtual_arcs(all_nets)
        with open('virtual_arcs.txt', 'w') as fp:
            fp.write(virtual_arcs)

    lang += virtual_arcs
    lang += "}"
    return lang


def get_json(node):
    if isinstance(node, Place):
        return node.data
    elif isinstance(node, Transition):
        return node.data.json


def set_checked_node(node: str):
    global checked_nodes
    checked_nodes.append(node)


def get_graph_metadata(petriNet: PetriNet, graph_id=None):
    meta_data = []
    if graph_id is not None:
        obj_manager = ObjectManager(f"./db/{graph_id}/running_logs")
        meta_data.append(("Places", len(list(petriNet.place()))))
        meta_data.append(("Transitions", len(list(petriNet.transition()))))
        meta_data.append(("Objects", obj_manager.num_objects()))
    else:
        obj_manager = ObjectManager("../running_logs")
        meta_data.append(("Places", len(list(petriNet.place()))))
        meta_data.append(("Transitions", len(list(petriNet.transition()))))
        meta_data.append(("Objects", obj_manager.num_objects()))

    num_children_transitions = 0
    for transition in petriNet.transition():
        if len(transition.output_arc()) == 0:
            num_children_transitions += 1

    meta_data.append(("Interaction paths", num_children_transitions))
    meta_data.append(("Root Places", len(petriNet.root)))
    return meta_data


# region Export
global merged_net
global metadata


def load_graph(graph_id=None):
    # merged_net
    global merged_net
    net_files = files.get_petri_net_files(graph_id)
    if net_files is None:
        logger.error(f"{graph_id} is not existed.")
        return None
    merged_net = PetriNet.load(net_files[0])
    for idx in range(1, len(net_files)):
        merged_net = PetriNet.merge(merged_net, PetriNet.load(net_files[idx]))
    # all nets
    all_nets = [PetriNet.load(net_files[0])]
    for idx in range(1, len(net_files)): all_nets.append(PetriNet.load(net_files[idx]))
    # metadata
    global metadata
    metadata = get_graph_metadata(merged_net, graph_id)
    content = build_graphviz(merged_net, all_nets)
    return content


def get_node(name):
    global merged_net
    logger.debug(f"Get node with name~{name}")
    return merged_net.node(name)


def is_place(name):
    try:
        node = get_node(name)
        logger.debug(f"check is_place: {node}")
        if isinstance(node, Place):
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def get_node_data(name):
    try:
        node = get_node(name)
        data = get_json(node)
        if isinstance(data, PageData):
            data = data.__getstate__()
        return data
    except Exception as e:
        logger.debug(str(e))
        return None
# endregion

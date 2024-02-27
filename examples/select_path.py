from collections import namedtuple
from petrinet.PetriNet import  Place, Transition, PetriNet
Path = namedtuple('Trajectory', ['transitions', 'places', 'arcs'])

def select_path(petriNet: PetriNet, visited_places: list)-> Path:
    selected_path = {'transitions': [], 'places': [], 'arcs': []}
    current_place:Place = list(petriNet.root)[0]
    
    selected_path['places'].append(current_place)
    visited_places.append(current_place)
    while (len(current_place.output_arc()) > 0):
        next_transition: Transition = list(current_place.output_arc())[0].destination

        if len(next_transition.output_arc()) > 1:
            current_place: Place = None
            for arc in next_transition.output_arc():
                if arc.destination not in visited_places:
                    current_place = arc.destination
                    selected_path['arcs'].append(arc)
                    break
            if current_place is None:
                return Trajectory(transitions=selected_path['transitions'], places=selected_path['places']), visited_places
            selected_path['transitions'].append(next_transition)
            selected_path['places'].append(current_place)
            visited_places.append(current_place)
        elif len(next_transition.output_arc()) > 0:
            arc = list(next_transition.output_arc())[0]
            current_place = arc.destination
            selected_path['arcs'].append(arc)
            selected_path['transitions'].append(next_transition)
            selected_path['places'].append(current_place)
            visited_places.append(current_place)
        else:
            selected_path['transitions'].append(next_transition)
            break
    return Path(transitions=selected_path['transitions'], places=selected_path['places'], arcs=selected_path['arcs']), visited_places

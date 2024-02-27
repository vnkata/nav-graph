from repository.core import ObjectManager
import numpy as np

def LessStrictPlaceComparator(a, b, objManager: ObjectManager) -> bool:
    a_elements = list(map(objManager.get_object, a.data.object_uuids))
    b_elements = list(map(objManager.get_object, b.data.object_uuids))

    if (None in a_elements) or (None in b_elements):
        raise NotImplementedError("Non-Items exist !")

    union = []
    intersection =  []
    for ac in a_elements:
        if ac in b_elements:
            intersection.append(ac)

    for ac in a_elements:
        if ac not in union: union.append(ac)
    for bc in b_elements:
        if bc not in union: union.append(bc)

    if ((len(intersection) * 1.0) /  len(union) ) > 0.85:
        return True
    else:
        return False



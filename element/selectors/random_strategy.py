from element.Element import ActionableElement
from abc import abstractmethod

import numpy as np


class StrategySelector(object):
    def __init__(self, actionable_elements: list[ActionableElement], candidate_masks: list[bool]):
        self.actionable_elements = actionable_elements
        self.candidate_masks = candidate_masks

    @abstractmethod
    def select(self) -> ActionableElement:
        pass

class RandomStrategySelector(StrategySelector):
    def __init__(self, actionable_elements: list[ActionableElement], candidate_masks: list[bool]):
        super().__init__(actionable_elements, candidate_masks)
    
    def select(self) -> int:
        indices = np.where(np.array(self.candidate_masks) == True)[0]
        selected_idx = np.random.choice(indices)
        return selected_idx

class FormFirstStrategySelector(StrategySelector):
    """This strategy will perfer to select form elements to explore next (if it is possible) """

    def __init__(self, actionable_elements: list[ActionableElement], candidate_masks: list[bool]):
        super().__init__(actionable_elements, candidate_masks)
    
    def select(self) -> int:
        for idx, (m, actional_el) in enumerate(zip(self.candidate_masks, self.actionable_elements )):
            if actional_el.get_attribute('tag_name') == 'form' and m==True: return idx

        indices = np.where(np.array(self.candidate_masks) == True)[0]
        selected_idx = np.random.choice(indices)
        return selected_idx
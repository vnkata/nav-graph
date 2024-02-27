import re
import xmltodict as x2d
import os

class BaseAssertion:
    """
    Base class for assertions.
    Containing information about test action, input, output, and element selectors.

    Parameters
    ----------
    step: TestStep
        Input test step (class defined by @Thanh)
    project_path: str
        Project directory

    Example usage
    -------------
    >> project_path = < project_path >
    >> net = < Custom PetriNet >
    >> places = net.net.place()
    >> for place in places:
    >>     for c in place.constraint:
    >>         assertion = BaseAssertion(c, project_path)
    >>         print(assertion)
    """

    def __init__(self, step, project_path: str):
        self.__action = step.action
        self.__inputs = []
        self.__inputs = self.parse_input(step)
        self.__outputs = []
        element_path = self.parse_element()
        self.__element = os.path.basename(element_path)
        self.__test_name = os.path.basename(os.path.dirname(element_path))
        self.__selector_collection = self.parse_selector_collection(project_path)
        self.__selector_method = self.parse_selector_method(project_path)

    @property
    def action(self):
        return self.__action

    @property
    def element(self):
        return self.__element

    @property
    def test_name(self):
        return self.__test_name

    @property
    def selector_method(self):
        return self.__selector_method

    @selector_method.setter
    def selector_method(self, value):
        if value not in self.__selector_collection.keys():
            raise ValueError(
                f'Invalid selector. It should be one of: {self.__selector_collection.keys()}')
        else:
            self.__selector_method = value

    @property
    def inputs(self):
        return self.__inputs

    @property
    def outputs(self):
        return self.__outputs

    @property
    def selector_collection(self):
        return self.__selector_collection

    def get_input(self, index):
        """Get the input for the given index."""
        return self.__inputs[index]

    def get_output(self, index):
        """Get the output for the given index."""
        return self.__outputs[index]

    def parse_input(self, step):
        """Parse the original input to a more interpretable format."""

        result = []
        for input in step.input:
            if hasattr(input, 'code'):
                # first input should be code
                result.append({"code": input.code})
            else:
                result.append(
                    {"datatype": input.datatype, "value": input.value})
        return result

    def parse_element(self):
        """
        Parse the element from the input.
        The input containing the element, if it exists, is always the first element,
        which in turn a one-entry dictionary.
        """

        match = re.search(".*findTestObject\(\'(.+?)\'\)",
                          self.__inputs[0]["code"])
        if match:
            return match.group(1)
        else:
            raise Exception("Input does not contain any element.")

    def parse_selector_method(self, project_path):
        """Parse the current selector from the input."""
        with open(os.path.join(project_path, "Object Repository", self.test_name, self.element + ".rs")) as file:
            data = x2d.parse(file.read())

        if data.get('WebElementEntity', None) is not None:
            return data['WebElementEntity']['selectorMethod'].lower()
        else:
            return None

    def parse_selector_collection(self, project_path):
        """Parse the selector collection from the input."""

        with open(os.path.join(project_path, "Object Repository", self.test_name, self.element + ".rs"), "rt") as file:
            data = x2d.parse(file.read())

        result = {}
        if data.get('WebElementEntity', None) is not None:
            collection = data['WebElementEntity']['selectorCollection']['entry']
            for entry in collection:
                key_val = list(entry.values())
                key = key_val[0]
                value = key_val[1]
                result[key.lower()] = value
            result['xpath'] = {}
            xpaths = data['WebElementEntity']['webElementXpaths']
            for xpath in xpaths:
                result['xpath'][xpath['name']] = xpath['value']
        return result

    def __repr__(self):
        return f"""
            action: {self.__action},\n
            inputs: {self.__inputs},\n
            outputs: {self.__outputs},\n
            element: {self.__element},\n
            selector method: {self.__selector_method},\n
            selector collection: {self.__selector_collection},\n
        """

    def __str__(self):
        return self.__repr__()

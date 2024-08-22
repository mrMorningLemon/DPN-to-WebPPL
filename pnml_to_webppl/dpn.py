import pm4py
from xml.etree import ElementTree
from pnml_to_webppl.functions import utils
import warnings


class DPN:
    def __init__(self, dpn_file):
        self.dpn_file = dpn_file
        self.net, self.initial_marking, self.final_marking = pm4py.read_pnml(dpn_file)
        self.net = utils.rename_variable_names(self.net)
        self._get_invisible_transitions(dpn_file)
        self._get_variable_information(dpn_file)

    def _get_variable_information(self, dpn_file):
        self.variable_information = {}
        with open(dpn_file, "r") as dpn_file:
            pnml_content_corrected = dpn_file.read().strip()

        root_corrected = ElementTree.fromstring(pnml_content_corrected)
        # Iterate through each variable in the XML
        for variable in root_corrected.findall(".//variable"):
            # Extract the desired attributes
            name = variable.find("name").text
            self.variable_information[name] = {}
            if "maxValue" in variable.attrib:
                self.variable_information[name]["maxValue"] = float(variable.get("maxValue"))
            if "minValue" in variable.attrib:
                self.variable_information[name]["minValue"] = float(variable.get("minValue"))
            if "type" in variable.attrib:
                self.variable_information[name]["type"] = variable.get("type")
            else:
                warnings.warn(f"No type defined for {variable}!")

    def _get_invisible_transitions(self, dpn_file):
        self.invisible_transitions = []
        with open(dpn_file, "r") as dpn_file:
            pnml_content_corrected = dpn_file.read().strip()

        root_corrected = ElementTree.fromstring(pnml_content_corrected)
        for transition in root_corrected.findall(".//transition"):
            invisible = transition.get("invisible", "false")
            if invisible == "true":
                self.invisible_transitions.append(transition.get("id"))
            else:
                continue

    def get_variable_type(self, variable_name):
        if variable_name in self.variable_information:
            return self.variable_information[variable_name]["type"]
        else:
            return None

    def is_invisible(self, transition_name):
        return transition_name in self.invisible_transitions

    def get_sample(self, variable_name):
        if variable_name in self.variable_information and "sample" in self.variable_information[variable_name]:
            return self.variable_information[variable_name]["sample"]
        else:
            return "[]"

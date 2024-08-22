def log_transitions(function_str, variable_dict):
    # Start of the JS function template
    function_str += """var log_transition = function(transition) {\nif (globalStore.printTransitions) {\nprint(transition + " ["""

    # Dynamically append each variable part, correctly handling quotation marks
    variable_parts = [f"{key} = " + '"+ globalStore.' + f"{key}" + ' + "' for key in variable_dict]
    function_str += ', '.join(variable_parts)

    # Close the print statement and function
    function_str += "]\");\n}\n}\n\n"

    return function_str


def log_state(function_str, dpn, variable_dict):
    # Start of the JS function template
    function_str += """var log_state = function() {\nif (globalStore.logState) {\n"""
    places_list = list(dpn.net.places)

    m_part = "console.log(\"M["
    places_parts = [f"" + '"+ globalStore.' + f"{place}" + ' + "' for place in places_list]
    m_part += ', '.join(places_parts)
    m_part += "]\""
    function_str += m_part

    # Dynamically append each variable part, correctly handling quotation marks
    variable_parts = [f"{key} = " + '"+ globalStore.' + f"{key}" + ' + "' for key in variable_dict]
    function_str += " + \" V[" + ', '.join(variable_parts)
    function_str += "]\""

    function_str += ");\n}\n}\n\n"

    return function_str


def datatype_to_xml_tag(function_str):
    webppl_code = """
var getXMLtag = function (type) {
if (type.includes("Double")) {
return "float";
} else if (type.includes("Integer")) {
return "integer";
} else if (type.includes("Boolean")) {
return "boolean";
}
return "string";
}\n\n"""

    function_str += webppl_code

    return function_str


def log_event(function_str, variable_dict):
    # Start of the JS function template
    function_str += """var log_transition = function(transition) {\n"""

    function_str += """if (transition !== "None") {\n"""
    
    # Get data type and define tag variables
    for variable in variable_dict:
        function_str += f"var {variable}Tag = getXMLtag(globalStore.vars.{variable}.type);\n"

    # Add here the code to log the event
    function_str += 'globalStore.xesOutput += "<event>\\n";\n'
    function_str += 'globalStore.xesOutput +=  "<string key=\\"concept:name\\" value=\\"" + transition + "\\"/>\\n";\n'

    for variable in variable_dict:

        function_str += 'if (globalStore.' + variable + ' !== undefined && ' + ' globalStore.' + variable + ' !== null' + ') {\n'

        function_str += 'if (globalStore.vars.' + variable + '.valueMapping) {\n'
        function_str += f"var {variable}Value = globalStore.vars.{variable}.valueMapping[globalStore.{variable}] || globalStore.{variable};\n"
        function_str += 'globalStore.xesOutput +=  "<"' + " + " + variable + 'Tag' + " + " + '  " key=\\"' + variable + '\\" value=\\"" + ' + variable + 'Value' +  ' + "\\"/>\\n";\n'
        function_str += '}\n'
        function_str += 'else {\n'
        function_str += 'globalStore.xesOutput +=  "<"' + " + " + variable + 'Tag' + " + " + '  " key=\\"' + variable + '\\" value=\\"" + ' + 'globalStore.' + variable + ' + "\\"/>\\n";\n'
        function_str += '}\n'
        function_str += '}\n'

    function_str += 'globalStore.xesOutput +=  "</event>\\n";\n'
    function_str += 'globalStore.trace += globalStore.xesOutput;\n'

    # Close the print statement and function
    function_str += "}\n"
    function_str += "};\n\n"

    return function_str


def create_logging(function_str, dpn, verbose):
    if verbose:
        function_str = datatype_to_xml_tag(function_str)
        function_str = log_event(function_str, dpn.variable_information)

    return function_str

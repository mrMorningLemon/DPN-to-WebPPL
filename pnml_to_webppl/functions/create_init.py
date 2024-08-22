def init_global_information(function_str, verbose):

    function_str += f"globalStore.countEnabled = 0;\n"
    function_str += f'globalStore.trace = "";\n'

    return function_str


def init_places(function_str, net, initial_marking):
    places_list = list(net.places)
    for place in places_list:
        if place in initial_marking.keys():
            function_str += f"globalStore.{place} = {initial_marking[place]};\n"
        else:
            function_str += f"globalStore.{place} = 0;\n"

    function_str += "\n"

    return function_str


def init_transitions(function_str, net):
    for transition in net.transitions:
        transition_id = transition.name
        transition_name = transition.label
        function_str += f"globalStore.enabled_{transition_id} = false; // {transition_name}\n"

    function_str += "\n"

    for transition in net.transitions:
        transition_id = transition.name
        function_str += f"globalStore.fired_{transition_id} = 0;\n"

    function_str += "\n"

    return function_str


def init_variables(function_str, variable_dict):
    variables_str = ', '.join([f"{variable} : {variable_dict[variable]}" for variable in variable_dict])
    function_str += f"globalStore.vars = {{ {variables_str} }};\n\n"

    for key in variable_dict:
        if variable_dict[key]['type'] == "java.lang.Integer" or variable_dict[key]['type'] == "java.lang.Double":
            function_str += f"globalStore.{key} = 0;\n"
        elif variable_dict[key]['type'] == "java.lang.String":
            function_str += f"globalStore.{key} = '';\n"

    return function_str


def create_init_function(dpn, verbose):
    # Initialize the init function string
    function_str = "var init = function(){\n"

    # Initialize global information
    function_str = init_global_information(function_str, verbose)

    # Initialize places
    function_str = init_places(function_str, dpn.net, dpn.initial_marking)

    # Initialize transitions
    function_str = init_transitions(function_str, dpn.net)

    # Initialize variables
    function_str = init_variables(function_str, dpn.variable_information)

    # Close the function
    function_str += "}\n\n"

    return function_str

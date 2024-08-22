import pandas as pd
from pnml_to_webppl.functions.utils import get_pre_conditions


def get_enabling_conditions(net):
    places_array = []
    transition_array = []
    guards_array = []
    for transition in net.transitions:
        guard = transition.properties.get('guard', None)
        if guard is not None:
            guard = get_pre_conditions(guard, net)
            # from guard remove ( and ) and replace with nothing
            guard = guard.replace('(', '').replace(')', '')  # Remove later it is just a quick fix
            for arc in transition.in_arcs:
                places_array.append(arc.source)
                transition_array.append(transition.name)
                guards_array.append(guard)
        else:
            for arc in transition.in_arcs:
                places_array.append(arc.source)
                transition_array.append(transition.name)
                guards_array.append(None)

    df = pd.DataFrame(places_array, columns=['places'])
    df['transitions'] = transition_array
    df['guards'] = guards_array

    enabling_conditions = {}
    for transition in df['transitions'].unique():
        df_filtered = df[df['transitions'] == transition]
        conditions = []
        for _, row in df_filtered.iterrows():
            # Adjusting the condition to check for empty strings or NaN values in 'guards'
            if pd.notna(row['guards']) and row['guards'].strip() != '':
                condition = f"globalStore.{row['places']} > 0 && {row['guards']}"
            else:
                condition = f"globalStore.{row['places']} > 0"
            conditions.append(condition)
        enabling_conditions[transition] = " && ".join(conditions)

    return enabling_conditions


def generate_enabler_function(function_str, enabling_dict, verbose):
    for key, condition in enabling_dict.items():
        statistics_code = f"""globalStore.countEnabled = globalStore.countEnabled + 1;\n""" if verbose else ""
        statistics_code_else = f"""globalStore.countEnabled = globalStore.countEnabled - 1;\n""" if verbose else ""

        js_func = f"""var update_enabled_{key} = function() {{\nif({condition}) {{\nif (!globalStore.enabled_{key}) {{\nglobalStore.enabled_{key} = true;\n{statistics_code}}}\n}} else {{\nif (globalStore.enabled_{key}) {{\nglobalStore.enabled_{key} = false;\n{statistics_code_else}}}\n}}\n}}\n\n"""
        function_str += js_func

    return function_str


def create_enabler_function(function_str, dpn, verbose):
    dict_enabling_conditions = get_enabling_conditions(dpn.net)

    function_str = generate_enabler_function(function_str, dict_enabling_conditions, verbose)

    function_str += "\n"

    return function_str

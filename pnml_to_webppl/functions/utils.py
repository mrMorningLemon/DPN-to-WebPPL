from pnml_to_webppl.dpn import DPN
import re

VARIABLE_PRIME_PATTERN = "globalStore.{variable}"
VARIABLE_OLD_PATTERN = "old_var_{variable}"


def get_firing_var_mapping(net):
    variable_mapping = {
        var["name"] + "'": VARIABLE_PRIME_PATTERN.format(
            variable=var["name"]) for var in net.properties.get('variables', [])}
    old_variable_mapping = {var["name"]: VARIABLE_OLD_PATTERN.format(
        variable=var["name"]) for var in net.properties.get('variables', [])}
    variable_mapping.update(old_variable_mapping)
    return variable_mapping


def replace_variables(string, net):
    variable_mapping = get_firing_var_mapping(net)
    text_list = [string]
    operators = ["&&", "||", "<=", ">=", "!=", "<", ">", "==", "+", "-", "(", ")"]
    for operator in operators:
        text_list = _splitby_and_add(text_list, operator)
    text_list = [variable_mapping[t] if t in variable_mapping else t for t in text_list]

    return "".join(text_list)


def get_pre_conditions(string, net):
    prime_variables = [
        var["name"] + "'" for var in net.properties.get('variables', [])]
    variable_mapping = {var["name"]: VARIABLE_PRIME_PATTERN.format(
        variable=var["name"]) for var in net.properties.get('variables', [])}
    subformulas = _get_subformulas(string)
    text_list = []
    for subformula in subformulas:
        if len(list(set(subformula) & set(prime_variables))) == 0:
            text_list.append("".join([variable_mapping[t] if t in variable_mapping else t for t in subformula]))
    return "&&".join(text_list)


def get_post_conditions(string, net):
    prime_variables = [
        var["name"] + "'" for var in net.properties.get('variables', [])]
    variable_mapping = {
        var["name"] + "'": VARIABLE_PRIME_PATTERN.format(
            variable=var["name"]) for var in net.properties.get('variables', [])}
    old_variable_mapping = {var["name"]: VARIABLE_OLD_PATTERN.format(
        variable=var["name"]) for var in net.properties.get('variables', [])}
    variable_mapping.update(old_variable_mapping)
    subformulas = _get_subformulas(string)
    text_list = []
    for subformula in subformulas:
        if len(list(set(subformula) & set(prime_variables))) > 0:
            text_list.append("".join([variable_mapping[t] if t in variable_mapping else t for t in subformula]))

    # For item in text_list remove ( and ) and replace with nothing
    text_list = [item.replace('(', '').replace(')', '') for item in text_list]  # Remove later it is just a quick fix

    return "&&".join(text_list)


def _get_subformulas(text):
    operators = ["&&", "||"]
    pattern = '|'.join(map(re.escape, operators))
    text_list = re.split(pattern, text)
    operators = ["<=", ">=", "<", ">", "!=", "==", "+", "-", "(", ")"]
    subformulas = []
    for subform in text_list:
        subform = [subform]
        for operator in operators:
            subform = _splitby_and_add(subform, operator)
        subformulas.append(subform)
    return subformulas


def _splitby_and_add(stringlist, token):
    new_string_list = []
    for index, value in enumerate(stringlist):
        splitted = value.split(token)
        for isplit, valsplit in enumerate(splitted):
            new_string_list.append(valsplit.strip())
            if isplit != len(splitted) - 1:
                new_string_list.append(token)
    return new_string_list


def replace_with_dict(text, replace_dict):
    for pattern, replacement in replace_dict.items():
        text = re.sub(pattern, replacement, text)
    return text


def rename_variable_names(net):
    replace_dict = {
        r'(\w):(\w)': r'\1__\2',  # Replace ':' between words with '__'
    }
    for v in net.properties.get('variables', []):
        v["name"] = replace_with_dict(v["name"], replace_dict)
    for transition in net.transitions:
        if "guard" in transition.properties:
            transition.properties["guard"] = replace_with_dict(transition.properties["guard"], replace_dict)
    return net


if __name__ == '__main__':
    dpn = DPN("../../examples/data/RoadFines_WithData.pnml")
    boolean_condition = "amount<=amount &&c == 'delayJudge' && a == 'test test' && a >= (delayPrefecture'+delayPrefecture) && (a<totalPaymentAmount && b<v) && totalPaymentAmount>=amount'"
    print(boolean_condition)
    print(replace_variables(boolean_condition, dpn.net))
    print(get_pre_conditions(boolean_condition, dpn.net))
    print(get_post_conditions(boolean_condition, dpn.net))

    dpn = DPN("../../examples/data/daily_activityV1_5.pnml")

    rename_variable_names(dpn.net)

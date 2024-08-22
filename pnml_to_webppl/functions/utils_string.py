from pnml_to_webppl.dpn import DPN
from pnml_to_webppl.functions import utils_eq_operators
import re
import itertools


def string_to_long(dpn):
    for var in [k for k,v in dpn.variable_information.items() if v["type"] == "java.lang.String"]:
        var_values = list(utils_eq_operators.get_vals(dpn.net,var))
        dpn = _replace_in_guards(dpn,var, var_values)
        dpn = _replace_in_var_desc(dpn,var_values, var)
    return dpn


def _replace_in_guards(dpn,var, var_values):
    reg_pattern = r"{var}\s*{op}\s*[\',\"]{val}[\',\"]"
    repl_pattern = "{var}{op}{val}"
    vars = [var,var+"\'"]
    ops = ["==","!="]
    for transition in dpn.net.transitions:
        if "guard" in transition.properties:
            guard = transition.properties["guard"]
            for var,op,val in itertools.product(vars, ops, var_values):
                guard = re.sub(reg_pattern.format(var=var,op=op,val=val), repl_pattern.format(var=var,val=var_values.index(val),op=op), guard)
            transition.properties["guard"] = guard
    return dpn


def _replace_in_var_desc(dpn,var_values,var):
    dpn.variable_information[var]["type"] = "java.lang.Long"
    dpn.variable_information[var]["minVale"] = 0
    dpn.variable_information[var]["maxValue"] = len(var_values)
    dpn.variable_information[var]["valueMapping"] = {i:v for i,v in enumerate(var_values)}
    return dpn


if __name__ == '__main__':
    dpn = DPN("../../examples/data/RoadFines_WithData.pnml")
    boolean_condition = "o' < delayJudge &&t' == 'delayJudge' && a == 'test test' && a >= (t'+delayPrefecture) && (t'==totalPaymentAmount && b<v)"
    dpn = string_to_long(dpn)
    print(dpn)
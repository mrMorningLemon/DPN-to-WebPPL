from pnml_to_webppl.dpn import DPN
from pnml_to_webppl.functions import utils, utils_eq_operators

IN_ARC_CODE = "globalStore.{place} = globalStore.{place} - 1;"
OUT_ARC_CODE = "globalStore.{place} = globalStore.{place} + 1;"
FIRING_STATISTICS_CODE = "globalStore.fired_{transition} = globalStore.fired_{transition} + 1;"
UPDATE_ENABLED_CODE = "update_enabled_{transition}();"
FIRING_CODE = "var fire_{transition} = function() {{\n{code}\n}}"

WRITE_VARIABLES_OLD_VALUE_CODE = "var old_var_{write_variable} = globalStore.{write_variable};"
WRITE_VARIABLES_GEN_VALUE_INTEGER_CODE = "globalStore.{write_variable} = randomInteger({{n: globalStore.vars['{write_variable}']['maxValue']}});"
WRITE_VARIABLES_GEN_VALUE_DOUBLE_CODE = "globalStore.{write_variable} = uniform({{a: globalStore.vars['{write_variable}']['minValue'], b: globalStore.vars['{write_variable}']['maxValue']}});"
WRITE_VARIABLES_GEN_VALUE_STRING_CODE = "globalStore.{write_variable} = sample(Categorical({{vs: [{samples}]}}));"
WRITE_VARIABLES_write_VALUE_CODE = "globalStore.{write_variable} = {value};"
WRITE_VARIABLES_CONDITION = "condition({guard});"


def generate_firings(dpn):
    firings = [_generate_firing(dpn, transition) for transition in dpn.net.transitions]
    return "\n\n".join(firings)+"\n"


def _generate_firing(dpn, transition):
    firing = [_gen_tokenmove(transition),_gen_statistics(transition),_gen_write_variables(transition,dpn),
              _gen_update_transitions(transition)]
    return FIRING_CODE.format(code="\n".join(firing),transition=transition.name)+"\n"


def _gen_tokenmove(transition):
    in_arc_moves = [IN_ARC_CODE.format(place=in_arc.source) for in_arc in transition.in_arcs]
    out_arc_moves = [OUT_ARC_CODE.format(place=out_arc.target) for out_arc in transition.out_arcs]
    return "\n\n".join(in_arc_moves) + "\n" + "\n\n".join(out_arc_moves)+"\n"


def _gen_statistics(transition):
    return FIRING_STATISTICS_CODE.format(transition=transition.name)+"\n"


def _gen_update_transitions(transition):
    transitions_to_update = list(set([out_arc.target.name for in_arc in transition.in_arcs for out_arc in in_arc.source.out_arcs] + [in_arc.target.name for out_arc in transition.out_arcs for in_arc in out_arc.target.out_arcs]))
    return "\n".join([UPDATE_ENABLED_CODE.format(transition=transition) for transition in transitions_to_update])


def _gen_write_variables(transition, dpn):
    write_variables = []
    if "writeVariable" in transition.properties:
        for write_variable in transition.properties["writeVariable"]:
            eq_op = utils_eq_operators.get_eq_write_val(transition.properties["guard"], dpn.net,write_variable) if "guard" in transition.properties else None
            write_variables.append(WRITE_VARIABLES_OLD_VALUE_CODE.format(write_variable=write_variable))
            if eq_op == None or len(eq_op) == 0:
                if dpn.get_variable_type(write_variable) in ["java.lang.Integer","java.lang.Long"]:
                    write_variables.append(WRITE_VARIABLES_GEN_VALUE_INTEGER_CODE.format(write_variable=write_variable))
                elif dpn.get_variable_type(write_variable) == "java.lang.Double":
                    write_variables.append(WRITE_VARIABLES_GEN_VALUE_DOUBLE_CODE.format(write_variable=write_variable))
                elif dpn.get_variable_type(write_variable) == "java.lang.String":
                    write_variables.append(WRITE_VARIABLES_GEN_VALUE_STRING_CODE.format(write_variable=write_variable,samples=dpn.get_sample(write_variable)))
            else:
                write_variables.append(WRITE_VARIABLES_write_VALUE_CODE.format(write_variable=write_variable,value=eq_op[0]))
        if "guard" in transition.properties:
            write_variables.append(WRITE_VARIABLES_CONDITION.format(guard=utils.get_post_conditions(transition.properties["guard"], dpn.net)))
    return "\n".join(write_variables)+"\n"


if __name__ == '__main__':
    dpn = DPN("../../examples/data/simple_auction.pnml")
    print(generate_firings(dpn))

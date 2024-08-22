import ast
from pnml_to_webppl.functions import utils
from pnml_to_webppl.dpn import DPN


# Function to recursively find all value pairs with '=='
def _find_equality_pairs(node, astop=ast.Eq):
    pairs = []
    # Check if the current node is a Boolean operation
    if isinstance(node, ast.BoolOp):
        for value in node.values:
            pairs.extend(_find_equality_pairs(value))
    # Check if the current node is a Compare operation and specifically looking for '=='
    elif isinstance(node, ast.Compare) and any(isinstance(op, astop) for op in node.ops):
        left = ast.unparse(node.left)
        # Assuming there could be multiple comparisons, though for '==' it's usually one
        for comparator in node.comparators:
            right = ast.unparse(comparator)
            pairs.append((left, right))
    return pairs


def _get_eq_vals(logical_formula, net, astop):
    logical_formula = _convert_log_form(net, logical_formula)
    modified_formula = logical_formula.replace("&&", " and ").replace("||", " or ")
    # Parse the modified formula into an AST
    parsed_ast = ast.parse(modified_formula, mode='eval')
    # Find all value pairs with '=='
    equality_pairs = _find_equality_pairs(parsed_ast.body, astop)
    equality_pairs_dict = {k: [] for (k, _) in equality_pairs}
    for (k, v) in equality_pairs: equality_pairs_dict[k].append(v)
    return equality_pairs_dict


def get_eq_val(logical_formula, net, variables, astop=ast.Eq):
    res = {}
    for var in variables:
        variable = utils.get_firing_var_mapping(net)[var] if var in utils.get_firing_var_mapping(net) else var
        pairs = _get_eq_vals(logical_formula, net, astop)
        res[var] = pairs[variable] if variable in pairs else []
    return res


def get_eq_write_val(logical_formula, net, variable):
    variable = utils.VARIABLE_PRIME_PATTERN.format(variable=variable)
    return get_eq_val(logical_formula, net, [variable])[variable]


def get_neq_write_val(logical_formula, net, variable):
    variable = utils.VARIABLE_PRIME_PATTERN.format(variable=variable)
    return get_eq_val(logical_formula, net, [variable], ast.NotEq)[variable]


def get_vals(net, variable):
    old_var = utils.VARIABLE_OLD_PATTERN.format(variable=variable)
    prime_var = utils.VARIABLE_PRIME_PATTERN.format(variable=variable)
    var_vals = []
    for transition in net.transitions:
        if "guard" in transition.properties:
            var_vals_dict = get_eq_val(transition.properties["guard"], net, [old_var, prime_var])
            var_vals.extend(var_vals_dict[prime_var])
            var_vals.extend(var_vals_dict[old_var])
            var_vals_dict = get_eq_val(transition.properties["guard"], net, [old_var, prime_var])
            var_vals.extend(var_vals_dict[prime_var])
            var_vals.extend(var_vals_dict[old_var])
    return set([v[1:len(v) - 1] for v in var_vals])


def _convert_log_form(net, logical_formula):
    return utils.replace_variables(logical_formula, net)


if __name__ == '__main__':
    dpn = DPN("../../examples/data/simple_auction.pnml")
    boolean_condition = "o' < delayJudge &&t' == 'delayJudge' && a == 'test test' && a >= (t'+delayPrefecture) && (t'==totalPaymentAmount && b<v)"
    print(boolean_condition)
    print(get_eq_write_val(boolean_condition, dpn.net, "t"))
    dpn = DPN("../../examples/data/RoadFines_WithData.pnml")
    print(get_vals(dpn.net, "dismissal"))

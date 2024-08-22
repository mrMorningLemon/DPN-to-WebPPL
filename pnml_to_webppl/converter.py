import pnml_to_webppl.functions.create_init as init_function
import pnml_to_webppl.functions.create_enabler as enabler_function
from pnml_to_webppl.dpn import DPN
from pnml_to_webppl.functions.create_logging import create_logging as logging_function
from pnml_to_webppl.functions.create_simulator import create_simulator_function, create_simulator_loop_function
import pnml_to_webppl.functions.create_firing as firing_function
from pnml_to_webppl.functions import utils_string


def convert_dpn_to_webPPL(path, verbose, simulation_steps, sample_size):
    # Load dpn class
    dpn = DPN(path)

    dpn = utils_string.string_to_long(dpn)

    # Create Initial Function
    function_str = init_function.create_init_function(dpn, verbose)

    # Create Enabler Function
    function_str = enabler_function.create_enabler_function(function_str, dpn, verbose)

    # Create Firings Function
    function_str += firing_function.generate_firings(dpn)

    # Create Logging
    function_str = logging_function(function_str, dpn, verbose)

    # Create Simulator Loop Function
    function_str = create_simulator_loop_function(function_str, dpn, verbose)

    # Create Simulation Function
    function_str = create_simulator_function(function_str, simulation_steps, sample_size, dpn, verbose)

    return function_str

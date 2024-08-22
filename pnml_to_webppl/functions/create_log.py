import os
import subprocess
import sys


def create_log_header():
    log_header = """<?xml version="1.0" encoding="utf-8" ?>
<log xes.version="1849-2016" xes.features="nested-attributes" xmlns="http://www.xes-standard.org/">
<extension name="Organizational" prefix="org" uri="http://www.xes-standard.org/org.xesext" />
<extension name="Time" prefix="time" uri="http://www.xes-standard.org/time.xesext" />
<extension name="Concept" prefix="concept" uri="http://www.xes-standard.org/concept.xesext" />
<extension name="Lifecycle" prefix="lifecycle" uri="http://www.xes-standard.org/lifecycle.xesext" />
<string key="origin" value="csv" />\n"""

    return log_header


def generate_trace_ids(event_log):
    event_log_list = event_log.split("\n")

    # Get the trace ids
    trace_id = 0
    for line in event_log_list:
        if "<trace>" in line:
            trace_id += 1
            # append the trace id as the next element in the
            event_log_list[event_log_list.index(line)] = line + f"\n<string key=\"concept:name\" value=\"{trace_id}\"/>"

    event_log = "\n".join(event_log_list)

    return event_log


def generate_event_log(path_to_webppl, full_path):
    event_log = create_log_header()
    command = [path_to_webppl, full_path]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        result = result.stdout.split("\n")

        # If line does not start with "<" and ends with ">" print it
        for line in result:
            if not line.startswith("<") and not line.endswith(">") and not line == "undefined":
                print(line)

        # Remove each element that does not start with "<" and ends with ">"
        result = [line for line in result if line.startswith("<") and line.endswith(">")]

        # Remove last occurrences after </trace> to avoid incomplete traces
        last_index = len(result) - 1 - result[::-1].index('</trace>')
        result = result[:last_index + 1]
        result = "\n".join(result)
        event_log += result
        event_log += "\n</log>"

    except subprocess.CalledProcessError as e:
        # If an error occurs, print the error output
        print("Error occurred while checking WebPPL version:")
        print(e.stderr)

    event_log = generate_trace_ids(event_log)
    return event_log


def find_npm_global_path():
    # Determine if the operating system is Windows
    is_windows = sys.platform.startswith('win')

    # Construct the command based on the operating system
    command = "npm config get prefix"

    try:
        # Run the command to get the global install prefix
        npm_prefix = subprocess.check_output(command, shell=True, text=True).strip()

        # Append the path to the 'bin' directory based on OS
        if is_windows:
            webppl_path = os.path.join(npm_prefix, 'webppl.cmd')  # Windows uses .cmd or .bat
        else:
            webppl_path = os.path.join(npm_prefix, 'bin', 'webppl')  # Unix systems use 'bin' directory

        return webppl_path
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
        return None

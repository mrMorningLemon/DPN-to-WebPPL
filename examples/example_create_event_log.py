import os
from pnml_to_webppl.functions.create_log import generate_event_log
from pnml_to_webppl.functions.create_log import find_npm_global_path


# Run the webPPL file
full_path = os.path.abspath('examples/webppl_files/simple_auction.wppl')
print(full_path)
# Find path to webppl executable on your system
# Usually the path looks like this: C:\Users\...\AppData\Roaming\npm\webppl.cmd for windows machines
path_to_webppl = find_npm_global_path()


synthetic_log = generate_event_log(path_to_webppl, full_path)

# Save the synthetic log to a file
with open('examples/xes_files/simple_auction.xes', 'w') as f:
    f.write(synthetic_log)

import os
from pnml_to_webppl.converter import convert_dpn_to_webPPL

# Initialize Path from examples data
path_pnml = os.path.abspath('../examples/data/simple_auction.pnml')

# Convert DPN to WebPPL
webPPL_file = convert_dpn_to_webPPL(path_pnml, verbose=True, simulation_steps=50, sample_size=5000)


# save as webPPL file in outpur folder
with open('examples/webppl_files/simple_auction.wppl', 'w') as f:
    f.write(webPPL_file)

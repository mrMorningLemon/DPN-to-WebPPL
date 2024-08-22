# Data Petri nets to WebPPL
This tool provides an efficient way to convert Petri Net Markup Language (PNML) files representing data Petri nets (DPNs) into WebPPL (Probabilistic Programming Language) scripts. It aims to facilitate the analysis and simulation of data-aware petri nets defined in PNML through the powerful inference capabilities of WebPPL. Also this tool can generate valid XES event logs out of a WebPPL file. 

## Using Docker

Detailed installation instructions are found further below.
For simplicity, we also provide a `Dockerfile` that takes care of all installation steps.
After installing and starting [Docker](https://www.docker.com/get-started/), it suffices to run the following from command line (in the directory of our artifact):

1. Build the docker container: `docker build -t bpm .`
2. Run the container in interactive mode: `docker run -it bpm /bin/bash`
3. One can now run scripts in the container as explained further below after the installation section. For example, to produce WebPPL code, which can be explored with [webppl](http://webppl.org), for our running example, it suffices to run the following:
```
python examples/example_create_webppl.py
```
The result webppl file is then found in `examples/webppl_files/simple_auction.wppl`:
```
cat examples/webppl_files/simple_auction.wppl
```

Similarly, to produce an XES event log for our running example, it suffices to run the following script in the docker container:
```
python examples/example_create_event_log.py
```
The resulting XES file can be accessed as follows:
```
cat examples/xes_files/simple_auction.xes
```

To exit the docker container, it suffices to run `exit`.

## Installation
To use the DPN to WebPPL Converter, ensure that you have Python 3.x installed on your system. Follow these steps to set up the converter:

1. Download and install Node.js (which includes npm) from the official Node.js website (https://nodejs.org/en). Choose the LTS (Long Term Support) version for the most stable and supported setup. After installation, you can verify that Node.js and npm are correctly installed by running the following commands in your command line:
```bash
node -v
npm -v
```

2. Once Node.js and npm are installed, you can install WebPPL globally using npm. You can install WebPPL by following the instructions. 
```bash
npm install -g webppl
```

3. Clone the repository to your local machine using the following command or by downloading the repository as a zip file and extracting it to a local directory:
```bash
git clone <repository-anonymized>
```

4. Navigate to the root directory of the repository: 
```bash
cd <repository-name>
```

5. Install the required dependencies using the following command:
```bash
pip install -r requirements.txt
```



# Convert PNML to WebPPL
To convert a PNML file to a WebPPL script, follow the example provided below. This example assumes you have a valid PNML file located in the 'examples/data/' directory. New PNML files can be added to the 'examples/data/' directory.
As an example to test the converter, you can run the Python file in 'examples/example_create_webppl.py'. The content of the file is shown below. 
```python
import os
from pnml_to_webppl.converter import convert_dpn_to_webPPL

# Initialize Path for the PNML file
path_pnml = os.path.abspath('examples/data/simple_auction.pnml')

# Convert DPN to WebPPL
webPPL_file = convert_dpn_to_webPPL(path_pnml, verbose=False, simulation_steps=10)

print(webPPL_file)

# Save the WebPPL code to a file in the output folder
with open('simple_auction.wppl', 'w') as f:
    f.write(webPPL_file)
```
After execution a file named 'simple_auction.wppl' will be created in the directory. The content of the file will be the WebPPL script generated from the PNML file and can be pasted into the console of http://webppl.org to test it or used in our application to generate a XES event log. Notice that webPPL might give initialization warnings, particularly if a huge sample size, data domain, or step size is chosen. Those warnings indicate that many samples are discarded, which might penalize performance. The warnings should not be interpreted as an error. Rather, they indicate that one wants to refine the model by e.g. further restricting data domains, or adjusting the simulation's parameters.

# Generate XES Event Log from WebPPL
To generate a XES event log from a WebPPL script, the example provided below can be followed. This example assumes you have a valid WebPPL script located in the 'examples/webppl_files/' directory. The function "find_npm_global_path()" finds the local execution file of the WebPPL installation. This path can also be provided manually.
As an example to test the converter, you can run the Python file in 'examples/example_create_event_log.py'. The content of the file is shown below. Some examples of already generated event logs using this method can be found in the 'examples/xes_files/' directory.

```python
import os
from pnml_to_webppl.functions.create_log import generate_event_log
from pnml_to_webppl.functions.create_log import find_npm_global_path


# Run the webPPL file
full_path = os.path.abspath('webppl_files/simple_auction.wppl')
print(full_path)
# Find path to webppl executable on your system
# Usually the path looks like this: C:\Users\...\AppData\Roaming\npm\webppl.cmd for windows machines
path_to_webppl = find_npm_global_path()


synthetic_log = generate_event_log(path_to_webppl, full_path)

# Save the synthetic log to a file
with open('xes_files/simple_auction.xes', 'w') as f:
    f.write(synthetic_log)

```
When the PNML file is complex and thus the resulting WebPPL file is complex, the generation of the XES-File can take a while and a initialization warning can appear. This can also happen if a huge sample size or simulator step size is chosen. Also, it is important to note that in this implementation only traces can be generated, that also reach the final marking. The tool will by default output two values: one boolean (`true`, if the WebPPL query has been answered; `false`, otherwise) and one real (probability of answering that query). The generated XES file can be opened with e.g. ProM to visualize the event log.



## Contributing
Due to the double-blind review process, we are unable to list specific contributing guidelines, authors, or the project's status. 

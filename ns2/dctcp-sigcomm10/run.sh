#!/bin/bash

# source settings.sh
python ./run_sim.py --fig_1 --fig_13 --fig_14
echo "Please navigate to:  http://<IP_ADDRESS>:8002 in your browser to view the results."
sudo python -m SimpleHTTPServer 8002


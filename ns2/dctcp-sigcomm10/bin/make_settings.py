#!/usr/bin/env python

import sys, os

SETTINGS_FILE = os.path.expandvars("settings.sh")

cwd = os.getcwd()

additions = """#!/bin/bash

################################
#### NS-2 v2.34 Environment ####
################################
NS2_PATH={0}/ns-2/ns-allinone-2.34
# LD_LIBRARY_PATH
OTCL_LIB=$NS2_PATH/otcl-1.13
NS2_LIB=$NS2_PATH/lib
X11_LIB=/usr/X11R6/lib
USR_LOCAL_LIB=/usr/local/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$OTCL_LIB:$NS2_LIB:$X11_LIB:$USR_LOCAL_LIB

# TCL_LIBRARY
TCL_LIB=$NS2_PATH/tcl8.4.18/library
USR_LIB=/usr/lib
export TCL_LIBRARY=$TCL_LIB:$USR_LIB

# PATH
XGRAPH=$NS2_PATH/bin:$NS2_PATH/tcl8.4.18/unix:$NS2_PATH/tk8.4.18/unix
NS=$NS2_PATH/ns-2.34/
NAM=$NS2_PATH/nam-1.14/
PATH=$PATH:$XGRAPH:$NS:$NAM

####################
#### DCTCP NS-2 ####
####################
export DCTCP_NS2={0}
export TCL_DIR=${{DCTCP_NS2}}/tcl
export PYTHONPATH="$PYTHONPATH:${{DCTCP_NS2}}/bin"
""".format(cwd)

with open(SETTINGS_FILE, 'w') as f:
    f.write(additions)



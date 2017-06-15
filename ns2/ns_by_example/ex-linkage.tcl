# Jae Chung  7-13-99

# Create MyAgent (This will give two warning messages that
# no default vaules exist for my_var1_otcl and my_var2_otcl)
set myagent [new Agent/MyAgentOtcl]

# Set configurable parameters of MyAgent
$myagent set my_var1_otcl 3
$myagent set my_var2_otcl 3.14

# Give a command to MyAgent
$myagent call-my-priv-func

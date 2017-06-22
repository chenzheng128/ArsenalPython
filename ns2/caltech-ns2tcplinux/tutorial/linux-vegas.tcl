#Create a simulator object
set ns [new Simulator]

#Create a bottleneck link.
set router_snd [$ns node]
set router_rcv [$ns node]
$ns duplex-link $router_snd $router_rcv 10Mb 10ms DropTail
$ns queue-limit $router_snd $router_rcv 10000
# Create two flows sharing the bottleneck link
for {set i 1} {$i <=3} {incr i 1} {
  #Create the sending nodes,the receiving nodes.
  set bs($i) [$ns node]
  $ns duplex-link $bs($i) $router_snd 100Mb 1ms DropTail
  set br($i) [$ns node]
  $ns duplex-link $router_rcv $br($i) 100Mb 1ms DropTail
  #setup sender side
  set tcp($i) [new Agent/TCP/Linux]
  $tcp($i) set timestamps_ true
  $tcp($i) set window_ 100000
  $ns at 0 "$tcp($i) select_ca vegas"
  $ns attach-agent $bs($i) $tcp($i)

  #set up receiver side
   set sink($i) [new Agent/TCPSink/Sack1]
  $sink($i) set ts_echo_rfc1323_ true
  $ns attach-agent $br($i) $sink($i)

  #logical connection
  $ns connect $tcp($i) $sink($i)

  #Setup a FTP over TCP connection
  set ftp($i) [new Application/FTP]
  $ftp($i) attach-agent $tcp($i)
  $ftp($i) set type_ FTP

  #Schedule the life of the FTP
  $ns at 0 "$ftp($i) start"
  $ns at 10 "$ftp($i) stop"
}

#change default parameters, all TCP/Linux will see the changes!
$ns at 3 "$tcp(1) set_ca_default_param vegas alpha 40"
$ns at 3 "$tcp(1) set_ca_default_param vegas beta 40"
# confirm the changes by printing the parameter values (optional)
$ns at 3 "$tcp(2) get_ca_default_param vegas alpha"
$ns at 3 "$tcp(2) get_ca_default_param vegas beta"


# change local parameters, only tcp(3) is affected. (optional)
$ns at 6 "$tcp(3) set_ca_param vegas alpha 20"
$ns at 6 "$tcp(3) set_ca_param vegas beta 20"
# confirm the changes by printing the parameter values (optional)
$ns at 6 "$tcp(3) get_ca_param vegas alpha"
$ns at 6 "$tcp(3) get_ca_param vegas beta"

#Schedule the stop of the simulation
$ns at 11 "exit 0"


#Start the simulation
$ns run

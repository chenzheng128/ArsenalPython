/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

// Network topology
//
//       n0    n1   n2   n3
//       |     |    |    |
//       =================
//              LAN
//
// - CBR/UDP flows from n0 to n1 and from n3 to n0
// - DropTail queues
// - Tracing of queues and packet receptions to file "csma-one-subnet.tr"

#include <iostream>
#include <fstream>

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/csma-module.h"
#include "ns3/applications-module.h"
#include "ns3/internet-module.h"

using namespace ns3;


bool firstCwnd = true;
bool firstSshThr = true;
bool firstRtt = true;
bool firstRto = true;
Ptr<OutputStreamWrapper> cWndStream;
Ptr<OutputStreamWrapper> ssThreshStream;
Ptr<OutputStreamWrapper> rttStream;
Ptr<OutputStreamWrapper> rtoStream;
Ptr<OutputStreamWrapper> nextTxStream;
Ptr<OutputStreamWrapper> nextRxStream;
Ptr<OutputStreamWrapper> inFlightStream;
uint32_t cWndValue;
uint32_t ssThreshValue;


NS_LOG_COMPONENT_DEFINE ("NodeApis");

// copy from csma-one-subnet
// change from UDP -> TCP
// time ./waf --run node-apis && wc -l statistics/node-apis.tr
// time ./waf --run node-apis && wc -l statistics/NodeApiTcp-TcpNewReno-cwnd.data

int printInterfaceAddress( Ipv4InterfaceContainer interfaces1){
  // using GetN to inter Ipv4InterfaceContainer
  NS_LOG_INFO("<Ipv4InterfaceContainer> Iterate interfaces ");
  uint32_t nNodes = interfaces1.GetN ();
  for (uint32_t i = 0; i < nNodes; ++i)
  {
    std::pair<Ptr<Ipv4>, uint32_t> pair = interfaces1.Get (i);
    //method (pair.first, pair.second);  // use the pair
    NS_LOG_INFO("  interfaces1 Get() pair " << pair.first << " " << pair.second);
    NS_LOG_INFO("    GetAddress() " << interfaces1.GetAddress(i, 0));
  }
  return 0;
}
int
main (int argc, char *argv[])
{
//
// Users may find it convenient to turn on explicit debugging
// for selected modules; the below lines suggest how to do this
//
#if 1
  LogComponentEnable ("NodeApis", LOG_LEVEL_INFO);
#endif
//
// Allow the user to override any of the defaults and the above Bind() at
// run-time, via command-line arguments
//
  CommandLine cmd;
  cmd.Parse (argc, argv);
//
// Explicitly create the nodes required by the topology (shown above).
//
  int k = 8;
  NS_LOG_INFO ("Create nodes.");
  NodeContainer allNodes;
  allNodes.Create (k);
  NS_LOG_INFO ( "Created " << k << " nodes ...");


  NS_LOG_INFO ("Build Topology");
  CsmaHelper csma;
  csma.SetChannelAttribute ("DataRate", DataRateValue (5000000));
  csma.SetChannelAttribute ("Delay", TimeValue (MilliSeconds (0.1)));
//
// Now fill out the topology by creating the net devices required to connect
// the nodes to the channels and hooking them up.
//
  NodeContainer nodes1;
  NodeContainer nodes2;
  for (int i = 0; i< k ; ++i)
  {
    if (i % 2 == 0)
    { // select half node to new Containers
      nodes1.Add(allNodes.Get(i));
      NS_LOG_INFO("add allNodes[" << i << "] to nodes group 1");
    }
    else
    {
      nodes2.Add(allNodes.Get(i));
      NS_LOG_INFO("add allNodes[" << i << "] to nodes group 2");
    }
    NS_LOG_INFO("node id: " << allNodes.Get(i)->GetId());
    //}
  }

  NetDeviceContainer devices1 = csma.Install (nodes1);
  NetDeviceContainer devices2 = csma.Install (nodes2);

  InternetStackHelper internet1;
  InternetStackHelper internet2;
  internet1.Install (nodes1);
  internet2.Install (nodes2);

// We've got the "hardware" in place.  Now we need to add IP addresses.
//
  NS_LOG_INFO ("Assign IP Addresses." << "10.1.1.0");
  Ipv4AddressHelper ipAddrs1;

  ipAddrs1.SetBase ("10.0.1.0", "255.255.255.0");
  Ipv4InterfaceContainer interfaces1 = ipAddrs1.Assign (devices1);
  Ipv4AddressHelper ipAddrs2;
  ipAddrs2.SetBase ("10.0.2.0", "255.255.255.0");
  Ipv4InterfaceContainer interfaces2 = ipAddrs2.Assign (devices2);
  // Ipv4AddressHelper 会自动记忆 ip 的分配状态自动递增, 如果继续使用 ipAddrs1 则会继续分配
  //Ipv4InterfaceContainer interfaces2 = ipAddrs1.Assign (devices2);

  printInterfaceAddress(interfaces1);
  printInterfaceAddress(interfaces2);

//
// Create an OnOff application to send UDP datagrams from node zero to node 1.
//
  NS_LOG_INFO ("Create Applications.");
  uint16_t port = 9;   // Discard port (RFC 863)

  OnOffHelper onoff ("ns3::TcpSocketFactory",
                     Address (InetSocketAddress (interfaces1.GetAddress (1), port)));
  onoff.SetConstantRate (DataRate ("500kb/s"));

  ApplicationContainer app = onoff.Install (nodes1.Get (0));
  // Start the application
  app.Start (Seconds (1.0));
  app.Stop (Seconds (60.0));

  // Create an optional packet sink to receive these packets
  PacketSinkHelper sink ("ns3::TcpSocketFactory",
                         Address (InetSocketAddress (Ipv4Address::GetAny (), port)));
  app = sink.Install (nodes1.Get (1));
  app.Start (Seconds (0.0));

//
// Create a similar flow from n3 to n0, starting at time 1.1 seconds
//
  onoff.SetAttribute ("Remote",
                      AddressValue (InetSocketAddress (interfaces1.GetAddress (0), port)));
  app = onoff.Install (nodes1.Get (3));
  app.Start (Seconds (1.1));
  app.Stop (Seconds (60.0));

  app = sink.Install (nodes1.Get (0));
  app.Start (Seconds (0.0));

  NS_LOG_INFO ("Configure Tracing.");

//
// Configure ascii tracing of all enqueue, dequeue, and NetDevice receive
// events on all devices.  Trace output will be sent to the file
// "csma-one-subnet.tr"
//
  AsciiTraceHelper ascii;
  csma.EnableAsciiAll (ascii.CreateFileStream ("statistics/NodeApiTcp.tr"));
  NS_LOG_INFO ( "create statistics/NodeApiTcp.tr file" );

//
// Also configure some tcpdump traces; each interface will be traced.
// The output files will be named:
//
//     csma-one-subnet-<node ID>-<device's interface index>.pcap
//
// and can be read by the "tcpdump -r" command (use "-tt" option to
// display timestamps correctly)
//

//enable of disable pcap tracing
#if 0
  csma.EnablePcapAll ("node-apis", false);
#endif


std::string prefix_file_name="statistics/NodeApiTcp";
std::string transport_prot = "TcpNewReno";
bool tracing=true;
if (tracing)
  {

      std::ofstream ascii;
      Ptr<OutputStreamWrapper> ascii_wrap;

      prefix_file_name += "-" +  transport_prot; // 文件名中增加 tcp类型
      NS_LOG_UNCOND("激活 tracing 文件记录 " << prefix_file_name);

      // ascii.open ((prefix_file_name + "-ascii.tr").c_str ());
      // ascii_wrap = new OutputStreamWrapper ((prefix_file_name + "-ascii").c_str (),
      //                                      std::ios::out);
      // stack.EnableAsciiIpv4All (ascii_wrap);

      //Simulator::Schedule (Seconds (0.00001), &TraceCwnd, prefix_file_name + "-cwnd.data");
      //Simulator::Schedule (Seconds (0.00001), &TraceSsThresh, prefix_file_name + "-ssth.data");
}
//
// Now, do the actual simulation.
//
  NS_LOG_INFO ("Run Simulation.");
  Simulator::Run ();
  Simulator::Destroy ();
  NS_LOG_INFO ("Done.");
}

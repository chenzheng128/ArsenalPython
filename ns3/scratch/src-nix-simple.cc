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

#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/ipv4-static-routing-helper.h"
#include "ns3/ipv4-list-routing-helper.h"
#include "ns3/ipv4-nix-vector-helper.h"
// gtk config support 
#include "ns3/gtk-config-store.h"

/*
 *  Simple point to point links:
 *
 *  n1 -- n2 -- n3 -- n4 -- n5 (new) - n6 (new)
 *
 *  n1 has UdpEchoClient
 *  n4 has UdpEchoServer (listen at :9)
 *  n5 has UdpEchoServer (listen at :109)
 *  n6 has OnOffServer   (listen at :209)
 *
 *  n1 IP: 10.1.1.1
 *  n2 IP: 10.1.1.2, 10.1.2.1
 *  n3 IP: 10.1.2.2, 10.1.3.1
 *  n4 IP: 10.1.3.2, 10.1.4.1
 *  n5 IP: 10.1.4.2, 10.1.5.1
 *  n6 IP: 10.1.5.2
 */

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("NixSimpleExample");


// Tracer 3个接口：文件全局变量， tracer记录，trace调度(Schedule在SocketList建立后注入)
Ptr<OutputStreamWrapper> cWndStream;
static void // copy function from tcp-large-transfer.cc
CwndTracer (uint32_t oldval, uint32_t newval)
{
  NS_LOG_UNCOND ("Tracer CwndTracer() Moving cwnd from " << oldval << " to " << newval);
}
static void
TraceCwnd (std::string cwnd_tr_file_name)
{
  AsciiTraceHelper ascii;
  cWndStream = ascii.CreateFileStream (cwnd_tr_file_name.c_str ());
  Config::ConnectWithoutContext (
      "/NodeList/*/$ns3::TcpL4Protocol/SocketList/*/CongestionWindow",
      MakeCallback (&CwndTracer));
}

static void SinkRx (Ptr<const Packet> p, const Address &ad) // copy func from topology-example-sim.cc
{
  Ipv4Header ipv4;
  p->PeekHeader (ipv4);
  // std::cout << "Tracer SinkRx() TTL: " << (unsigned)ipv4.GetTtl () << std::endl;
  std::cout << "Tracer SinkRx() src: " << ipv4.GetSource() << std::endl;
  // std::cout << "Tracer SinkRx() dst: " << ipv4.GetDestination () << std::endl;
}

int
main (int argc, char *argv[])
{
  bool debug = false;
  bool gtk_config = true;
  CommandLine cmd;
  cmd.AddValue ("debug", "debug 增加输出", debug);
  cmd.AddValue ("gtk_config", "使用 gtk-config 配置属性 ", gtk_config);
  cmd.Parse (argc, argv);


  //  copy code from tcp-large-transfer
  // Users may find it convenient to turn on explicit debugging
  // for selected modules; the below lines suggest how to do this
  //  LogComponentEnable("TcpL4Protocol", LOG_LEVEL_ALL);
  //  LogComponentEnable("TcpSocketImpl", LOG_LEVEL_ALL);
  //  LogComponentEnable("PacketSink", LOG_LEVEL_ALL);
  LogComponentEnable ("OnOffApplication", LOG_LEVEL_INFO);
  LogComponentEnable ("UdpEchoClientApplication", LOG_LEVEL_INFO);
  LogComponentEnable ("UdpEchoServerApplication", LOG_LEVEL_INFO);
  LogComponentEnable ("NixSimpleExample", LOG_LEVEL_ALL);
  if (debug)
    {
      LogComponentEnable ("Config", LOG_LEVEL_ALL);
    }

  NodeContainer nodes12;
  nodes12.Create (2);

  NodeContainer nodes23;
  nodes23.Add (nodes12.Get (1));
  nodes23.Create (1);

  NodeContainer nodes34;
  nodes34.Add (nodes23.Get (1));
  nodes34.Create (1);

  NodeContainer nodes45;
  nodes45.Add (nodes34.Get (1));
  nodes45.Create (1);

  NodeContainer nodes56;
  nodes56.Add (nodes45.Get (1));
  nodes56.Create (1);

  PointToPointHelper pointToPoint;
  pointToPoint.SetDeviceAttribute ("DataRate", StringValue ("5Mbps"));
  pointToPoint.SetChannelAttribute ("Delay", StringValue ("2ms"));

  NodeContainer allNodes = NodeContainer (nodes12, nodes23.Get (1), nodes34.Get (1), nodes45.Get(1),
          nodes56.Get(1));

  // NixHelper to install nix-vector routing
  // on all nodes
  Ipv4NixVectorHelper nixRouting;
  InternetStackHelper stack;
  #if 1 //enable or disable Nix Routing
  stack.SetRoutingHelper (nixRouting); // has effect on the next Install ()
  #endif
  stack.Install (allNodes);

  NetDeviceContainer devices12;
  NetDeviceContainer devices23;
  NetDeviceContainer devices34;
  NetDeviceContainer devices45;
  NetDeviceContainer devices56;
  devices12 = pointToPoint.Install (nodes12);
  devices23 = pointToPoint.Install (nodes23);
  devices34 = pointToPoint.Install (nodes34);
  devices45 = pointToPoint.Install (nodes45);
  devices56 = pointToPoint.Install (nodes56);

  Ipv4AddressHelper address1;
  address1.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4AddressHelper address2;
  address2.SetBase ("10.1.2.0", "255.255.255.0");
  Ipv4AddressHelper address3;
  address3.SetBase ("10.1.3.0", "255.255.255.0");
  Ipv4AddressHelper address4;
  address4.SetBase ("10.1.4.0", "255.255.255.0");
  Ipv4AddressHelper address5;
  address5.SetBase ("10.1.5.0", "255.255.255.0");

  Ipv4InterfaceContainer interfaces1 = address1.Assign (devices12);
  Ipv4InterfaceContainer interfaces2 = address2.Assign (devices23);
  Ipv4InterfaceContainer interfaces3 = address3.Assign (devices34);
  Ipv4InterfaceContainer interfaces4 = address4.Assign (devices45);
  Ipv4InterfaceContainer interfaces5 = address5.Assign (devices56);

  // Create router nodes, initialize routing database and set up the routing
  // tables in the nodes.
  #if 0
  //enable or disable Nix Routing
  Ipv4GlobalRoutingHelper::PopulateRoutingTables ();
  #endif

  // UdpEchoServerHelper Server and client 1
  NS_LOG_INFO("Setup Echo server at port 9, address " << interfaces3.GetAddress (1) );
  UdpEchoServerHelper echoServer (9);
  ApplicationContainer serverApps = echoServer.Install (nodes34.Get (1));
  serverApps.Start (Seconds (1.0));
  serverApps.Stop (Seconds (20.0));

  NS_LOG_INFO("Setup Echo Client( connet -> 9) at address " << interfaces1.GetAddress (0) );
  UdpEchoClientHelper echoClient (interfaces3.GetAddress (1), 9);
  echoClient.SetAttribute ("MaxPackets", UintegerValue (1));
  echoClient.SetAttribute ("Interval", TimeValue (Seconds (1.)));
  echoClient.SetAttribute ("PacketSize", UintegerValue (1024));
  ApplicationContainer clientApps = echoClient.Install (nodes12.Get (0));
  clientApps.Start (Seconds (1.0));
  clientApps.Stop (Seconds (20.0));

  // UdpEchoServerHelper Server and client 2
  NS_LOG_INFO("Setup Echo server at port 109, address " << interfaces4.GetAddress (1) );
  UdpEchoServerHelper echoServer2 (109);
  ApplicationContainer serverApps2 = echoServer2.Install (nodes45.Get (1));
  serverApps.Start (Seconds (1.0));
  serverApps.Stop (Seconds (20.0));
  // TODO 客户机要连接的地址 interfaces4.GetAddress (1) 与 服务器.Install节点 nodes45.Get (1) 如何能建立联系呢? 这样代码会更清晰一些
  NS_LOG_INFO("Setup Echo Client( connet -> 109) at address " << interfaces1.GetAddress (0) );
  UdpEchoClientHelper echoClient2 (interfaces4.GetAddress (1), 109); // 目标地址与端口
  echoClient2.SetAttribute ("MaxPackets", UintegerValue (1));
  echoClient2.SetAttribute ("Interval", TimeValue (Seconds (1.)));
  echoClient2.SetAttribute ("PacketSize", UintegerValue (1024));
  ApplicationContainer clientApps2 = echoClient2.Install (nodes12.Get (0));
  clientApps2.Start (Seconds (10.0));
  clientApps2.Stop (Seconds (20.0));

  // Tcp OnOffServer and Client setup; revised from examples/tcp/star.cc
  NS_LOG_INFO("Setup OnOff server at port 209, address " << interfaces5.GetAddress (1) );
  uint16_t port = 209;
  Address bindAddressAndPort (InetSocketAddress (Ipv4Address::GetAny (), port));
  PacketSinkHelper packetSinkHelper ("ns3::TcpSocketFactory", bindAddressAndPort);
  ApplicationContainer hubApp = packetSinkHelper.Install (nodes56.Get (1));
  hubApp.Start (Seconds (1.0));
  hubApp.Stop (Seconds (30.0));
  NS_LOG_INFO("Setup OnOff Node id="<<nodes12.Get(0)->GetId()<<" client (connet -> 209), address " << interfaces5.GetAddress (1) );
  OnOffHelper onOffHelper ("ns3::TcpSocketFactory", Address ());
  onOffHelper.SetAttribute ("OnTime", StringValue ("ns3::ConstantRandomVariable[Constant=1]"));
  onOffHelper.SetAttribute ("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=0]"));
  AddressValue remoteAddress (InetSocketAddress (interfaces5.GetAddress (1) , port));
  onOffHelper.SetAttribute ("Remote", remoteAddress);
  ApplicationContainer clientApps3 =  onOffHelper.Install (nodes12.Get(0));
  clientApps3.Start (Seconds (20.0));
  clientApps3.Stop (Seconds (20.03)); // 发2个包 , 每 0.1 秒 发一个

  Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpWestwood::GetTypeId ()));

  if (gtk_config)  // 使用 gtk_config 图形化配置属性
    {
      // 代码参考： https://www.nsnam.org/wiki/HOWTO_determine_the_path_of_an_attribute_or_trace_source
      GtkConfigStore configstore;
      configstore.ConfigureAttributes();
    }

  NS_LOG_INFO("设置完毕 ... \n进行仿真 ...");

  // add pcap tracing
  pointToPoint.EnablePcapAll("statistics/nix-simple", false);
  #if 0
  pointToPoint.EnableAsciiAll("statistics/nix-simple-ascii");
  #endif

  // Trace Connect 不能太早，如果 ApplicationList 还没初始化，则获取不到数据
  Config::ConnectWithoutContext ("/NodeList/*/ApplicationList/*/$ns3::PacketSink/Rx",
    MakeCallback (&SinkRx));

  // TraceCwnd 针对 socket 这种 tracer 必须通过 schedule 等候 socket 建立之后才能获取到数据
  Simulator::Schedule (Seconds (20.00001), &TraceCwnd,
                         "statistics/nix-simple-cwnd.data");

  // Trace routing tables
  Ptr<OutputStreamWrapper> routingStream = Create<OutputStreamWrapper> ("statistics/nix-simple.routes", std::ios::out);
  nixRouting.PrintRoutingTableAllAt (Seconds (8), routingStream);

  Simulator::Run ();
  Simulator::Destroy ();
  return 0;
}

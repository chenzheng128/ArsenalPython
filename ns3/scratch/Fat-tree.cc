// Construction of Fat-tree Architecture
// Authors: Linh Vu, Daji Wong

/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * Copyright (c) 2013 Nanyang Technological University
 *
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
 *
 * Authors: Linh Vu <linhvnl89@gmail.com>, Daji Wong <wong0204@e.ntu.edu.sg>
 */

#include <iostream>
#include <fstream>
#include <string>
#include <cassert>

#include "ns3/flow-monitor-module.h"
#include "ns3/bridge-helper.h"
#include "ns3/bridge-net-device.h"
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/ipv4-global-routing-helper.h"
#include "ns3/csma-module.h"
#include "ns3/ipv4-nix-vector-helper.h"
#include "ns3/gtk-config-store.h"
// ns-3.13-API
// #include "ns3/random-variable.h"
// ns-3.26-API
#include "ns3/random-variable-stream.h"

/*
 - This work goes along with the paper "Towards Reproducible Performance Studies of Datacenter Network Architectures Using An Open-Source Simulation Approach"

 - The code is constructed in the following order:
 1. Creation of Node Containers
 2. Initialize settings for On/Off Application
 3. Connect hosts to edge switches
 4. Connect edge switches to aggregate switches
 5. Connect aggregate switches to core switches
 6. Start Simulation

 - Addressing scheme:
 1. Address of host: 10.pod.switch.0 /24
 2. Address of edge and aggregation switch: 10.pod.switch.0 /16
 3. Address of core switch: 10.(group number + k).switch.0 /8
 (Note: there are k/2 group of core switch)

 - On/Off Traffic of the simulation: addresses of client and server are randomly selected everytime

 - Simulation Settings:
 - Number of pods (k): 4-24 (run the simulation with varying values of k)
 - Number of nodes: 16-3456
 - Simulation running time: 100 seconds
 - Packet size: 1024 bytes
 - Data rate for packet sending: 1 Mbps
 - Data rate for device channel: 1000 Mbps
 - Delay time for device: 0.001 ms
 - Communication pairs selection: Random Selection with uniform probability
 - Traffic flow pattern: Exponential random traffic
 - Routing protocol: Nix-Vector

 - Statistics Output:
 - Flowmonitor XML output file: Fat-tree.xml is located in the /statistics folder


 */

using namespace ns3;
using namespace std;
NS_LOG_COMPONENT_DEFINE("Fat-Tree");

// Function to create address string from numbers
//
char *
toString (int a, int b, int c, int d)
{

  int first = a;
  int second = b;
  int third = c;
  int fourth = d;

  char *address = new char[30];
  char firstOctet[30], secondOctet[30], thirdOctet[30], fourthOctet[30];
  //address = firstOctet.secondOctet.thirdOctet.fourthOctet;

  bzero (address, 30);

  snprintf (firstOctet, 10, "%d", first);
  strcat (firstOctet, ".");
  snprintf (secondOctet, 10, "%d", second);
  strcat (secondOctet, ".");
  snprintf (thirdOctet, 10, "%d", third);
  strcat (thirdOctet, ".");
  snprintf (fourthOctet, 10, "%d", fourth);

  strcat (thirdOctet, fourthOctet);
  strcat (secondOctet, thirdOctet);
  strcat (firstOctet, secondOctet);
  strcat (address, firstOctet);

  return address;
}

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
Ptr<OutputStreamWrapper> qlenStream;
uint32_t cWndValue;
uint32_t ssThreshValue;
uint32_t NODE_ID;

static void
SsThreshTracer (uint32_t oldval, uint32_t newval)
{
  // NS_LOG_DEBUG("Tracer SsThreshTracer() Moving ssth from " << oldval << " to " << newval);
  if (firstSshThr)
    {
      *ssThreshStream->GetStream () << "0.0 " << oldval << std::endl;
      firstSshThr = false;
    }
  *ssThreshStream->GetStream () << Simulator::Now ().GetSeconds () << " " << newval << std::endl;
  ssThreshValue = newval;

  if (!firstCwnd)
    {
      *cWndStream->GetStream () << Simulator::Now ().GetSeconds () << " " << cWndValue << std::endl;
    }
}

static void
RttTracer (Time oldval, Time newval)
{
  if (firstRtt)
    {
      *rttStream->GetStream () << "0.0 " << oldval.GetSeconds () << std::endl;
      firstRtt = false;
    }
  *rttStream->GetStream () << Simulator::Now ().GetSeconds () << " " << newval.GetSeconds ()
      << std::endl;
}

static void
RtoTracer (Time oldval, Time newval)
{
  if (firstRto)
    {
      *rtoStream->GetStream () << "0.0 " << oldval.GetSeconds () << std::endl;
      firstRto = false;
    }
  *rtoStream->GetStream () << Simulator::Now ().GetSeconds () << " " << newval.GetSeconds ()
      << std::endl;
}

static void
NextTxTracer (SequenceNumber32 old, SequenceNumber32 nextTx)
{
  *nextTxStream->GetStream () << Simulator::Now ().GetSeconds () << " " << nextTx << std::endl;
}

static void
InFlightTracer (uint32_t old, uint32_t inFlight)
{
  *inFlightStream->GetStream () << Simulator::Now ().GetSeconds () << " " << inFlight << std::endl;
}

static void
NextRxTracer (SequenceNumber32 old, SequenceNumber32 nextRx)
{
  *nextRxStream->GetStream () << Simulator::Now ().GetSeconds () << " " << nextRx << std::endl;
}

static void
TraceSsThresh (std::string ssthresh_tr_file_name)
{
  AsciiTraceHelper ascii;
  ssThreshStream = ascii.CreateFileStream (ssthresh_tr_file_name.c_str ());
  Config::ConnectWithoutContext ("/NodeList/*/$ns3::TcpL4Protocol/SocketList/*/SlowStartThreshold",
                                 MakeCallback (&SsThreshTracer));
}

static void
TraceRtt (std::string rtt_tr_file_name)
{
  AsciiTraceHelper ascii;
  rttStream = ascii.CreateFileStream (rtt_tr_file_name.c_str ());
  Config::ConnectWithoutContext ("/NodeList/*/$ns3::TcpL4Protocol/SocketList/*/RTT",
                                 MakeCallback (&RttTracer));
}

static void
TraceRto (std::string rto_tr_file_name)
{
  AsciiTraceHelper ascii;
  rtoStream = ascii.CreateFileStream (rto_tr_file_name.c_str ());
  Config::ConnectWithoutContext ("/NodeList/*/$ns3::TcpL4Protocol/SocketList/*/RTO",
                                 MakeCallback (&RtoTracer));
}

static void
TraceNextTx (std::string &next_tx_seq_file_name)
{
  AsciiTraceHelper ascii;
  nextTxStream = ascii.CreateFileStream (next_tx_seq_file_name.c_str ());
  Config::ConnectWithoutContext ("/NodeList/*/$ns3::TcpL4Protocol/SocketList/*/NextTxSequence",
                                 MakeCallback (&NextTxTracer));
}

static void
TraceInFlight (std::string &in_flight_file_name)
{
  AsciiTraceHelper ascii;
  inFlightStream = ascii.CreateFileStream (in_flight_file_name.c_str ());
  Config::ConnectWithoutContext ("/NodeList/*/$ns3::TcpL4Protocol/SocketList/*/BytesInFlight",
                                 MakeCallback (&InFlightTracer));
}

static void
TraceNextRx (std::string &next_rx_seq_file_name)
{
  AsciiTraceHelper ascii;
  nextRxStream = ascii.CreateFileStream (next_rx_seq_file_name.c_str ());
  Config::ConnectWithoutContext (
      "/NodeList/*/$ns3::TcpL4Protocol/SocketList/*/RxBuffer/NextRxSequence",
      MakeCallback (&NextRxTracer));
}

int
printInterfaceAddress (Ipv4InterfaceContainer interfaces1)
{
  // using GetN to inter Ipv4InterfaceContainer
  // NS_LOG_INFO("<Ipv4InterfaceContainer> Iterate interfaces ");
  std::cout << "    GetAddress() ";
  uint32_t nNodes = interfaces1.GetN ();
  for (uint32_t i = 0; i < nNodes; ++i)
    {
      std::pair<Ptr<Ipv4>, uint32_t> pair = interfaces1.Get (i);
      //method (pair.first, pair.second);  // use the pair
      // NS_LOG_INFO("  interfaces1 Get() pair " << pair.first << " " << pair.second);
      std::cout << " " << interfaces1.GetAddress (i, 0);
    }
  std::cout << "\n";
  return 0;
}

static void
CwndTracer (uint32_t oldval, uint32_t newval)
{
  // NS_LOG_DEBUG("Tracer CwndTracer() Moving cwnd from " << oldval << " to " << newval);

  if (firstCwnd)
    {
      *cWndStream->GetStream () << "0.0 " << oldval << std::endl;
      firstCwnd = false;
    }
  *cWndStream->GetStream () << Simulator::Now ().GetSeconds () << " " << newval << std::endl;
  cWndValue = newval;

  if (!firstSshThr)
    {
      *ssThreshStream->GetStream () << Simulator::Now ().GetSeconds () << " " << ssThreshValue
          << std::endl;
    }
}

static void
TraceCwnd (std::string cwnd_tr_file_name)
{
  AsciiTraceHelper ascii;
  cWndStream = ascii.CreateFileStream (cwnd_tr_file_name.c_str ());
  Config::ConnectWithoutContext ("/NodeList/*/$ns3::TcpL4Protocol/SocketList/*/CongestionWindow",
                                 MakeCallback (&CwndTracer));
}

static void
SinkRx (Ptr<const Packet> p, const Address &ad) // copy func from topology-example-sim.cc
{
  Ipv4Header ipv4;
  p->PeekHeader (ipv4);
  // std::cout << "Tracer SinkRx() TTL: " << (unsigned)ipv4.GetTtl () << std::endl;
  // std::cout << "Tracer SinkRx() src: " << ipv4.GetSource() << std::endl;
  // std::cout << "Tracer SinkRx() dst: " << ipv4.GetDestination () << std::endl;
}

void
TcPacketsInQueueTrace (uint32_t oldValue, uint32_t newValue)
{
  std::cout << "TcPacketsInQueue " << oldValue << " to " << newValue << std::endl;
}

void
DevicePacketsInQueueTrace (uint32_t oldValue, uint32_t newValue)
{
  NS_LOG_DEBUG( "DevicePacketsInQueue " << oldValue << " to " << newValue );
  *qlenStream->GetStream () << Simulator::Now ().GetSeconds () << " " << newValue << std::endl;
}



// Main function
//

int
main (int argc, char *argv[])
{

  //== 参数默认值
  //
  bool debug = false;               // 是否为 debug
  bool tracing = true;              // 是否 输出 tracing 数据
  bool UdpEchoTestOnly = false;     // using udp echo to test 使用UdpEcho测试各节点连通性, 否则改用 tcp 测试
  float duration = 60.0;            // 仿真时间 simulation seconds
  int num_flows = -1;               //随机流数量: -1 不限制randomflow数量, 其他值:限制randomflow数量
  bool flow_monitor = true;         // 是否记录 flow_monitor
  bool pcap = false;                // 是否记录 pcap
  bool ascii_trace = false;         // 是否记录 ascii trace
  float start_time = 0.1;           // 客户端发起时间, tracer 调度与它有关

  int k = 6;			                 // default number of ports per switch

  // Initialize parameters for On/Off application
  // Define variables for On/Off Application
  // These values will be used to serve the purpose that addresses of server and client are selected randomly
  int port = 9;
  int packetSize = 1024;		// 1024 bytes
  char dataRate_OnOff[] = "50Mbps";   // 50Mbs (cfi16)
  char maxBytes[] = "0";		// unlimited
  // Initialize parameters for Csma and PointToPoint protocol
  //
  char dataRate[] = "100Mbps";	// 1Gbps -> 100Mbs (cfi16)
  double delay = 0.001;		// 0.001 ms

  //== copy parameters setting from TcpVariantsComparison
  //
  std::string transport_prot = "TcpNewReno";
  double error_p = 0.0;
  std::string bandwidth = "5Mbps";
  std::string delay_str = "0.001ms";        // no use here , using delay instead of delay_str
  std::string access_bandwidth = "20Mbps";
  std::string access_delay = "45ms";
  std::string prefix_file_name = "statistics/fatTree";
  double data_mbytes = 0;
  uint32_t mtu_bytes = 400;
  uint32_t run = 0;
  std::string queue_disc_type = "ns3::PfifoFastQueueDisc";

  //== 临时修改一些初始化参数, 便于调试 debug 时  增加输出 或 加速测试
  debug = true;                     // 增加输出
  k = 6;                             // 调整节点数
  duration = 60.0 ;                 // 减小测试时间  60s-7m
  // num_flows = 1;               // 减小随机流数量

  //== 命令行传入参数 从 TcpVariantsComparison 复制而来
  //
  CommandLine cmd;
  cmd.AddValue ("k", "number of k ports per switch", k);
  cmd.AddValue ("debug", "debug 增加输出", debug);
  cmd.AddValue ("duration", "持续时长 Time to allow flows to run in seconds", duration);
  cmd.AddValue ("num_flows", "流数量 Number of flows", num_flows);
  cmd.AddValue ("tracing", "文件记录 Flag to enable/disable tracing", tracing);
  cmd.AddValue ("prefix_name", "Prefix of output trace file", prefix_file_name);
  cmd.AddValue ("flow_monitor", "Enable flow monitor", flow_monitor);
  cmd.AddValue ("pcap_tracing", "Enable or disable PCAP tracing", pcap);
  // TODO 下面这些参数还没对应使用
  cmd.AddValue ("error_p", "Packet error rate", error_p);
  cmd.AddValue ("bandwidth", "Bottleneck bandwidth", bandwidth);
  cmd.AddValue ("delay", "Bottleneck delay", delay_str);
  cmd.AddValue ("access_bandwidth", "Access link bandwidth", access_bandwidth);
  cmd.AddValue ("access_delay", "时延 Access link delay", access_delay);
  cmd.AddValue ("data", "Number of Megabytes of data to transmit", data_mbytes);
  cmd.AddValue ("mtu", "Size of IP packets to send in bytes", mtu_bytes);
  cmd.AddValue ("run", "Run index (for setting repeatable seeds)", run);
  cmd.AddValue ("queue_disc_type", "队列类型 Queue disc type for gateway (e.g. ns3::CoDelQueueDisc)", queue_disc_type);
  cmd.AddValue ("transport_prot", "Transport protocol to use: TcpNewReno, "
                "TcpHybla, TcpHighSpeed, TcpHtcp, TcpVegas, TcpScalable, TcpVeno, "
                "TcpBic, TcpYeah, TcpIllinois, TcpWestwood, TcpWestwoodPlus , TcpMyAlg (revised from Westwood)", transport_prot);
  cmd.Parse (argc, argv);

  // setting random seed
  SeedManager::SetSeed (1);
  SeedManager::SetRun (run);

  //== 调整日志输出
  //
  // LogComponentEnable ("OnOffApplication", LOG_LEVEL_INFO);
  LogComponentEnable ("UdpEchoClientApplication", LOG_LEVEL_INFO);
  LogComponentEnable ("UdpEchoServerApplication", LOG_LEVEL_INFO);
  if (debug)
    {
      LogComponentEnable ("Fat-Tree", LOG_LEVEL_ALL);
    }
  else
    {
      // TODO 暂时注释, 因为设置为 INFO 也会打印出 _DEBUG 信息, why?
      // LogComponentEnable ("Fat-Tree", LOG_LEVEL_INFO);
    }

  // 命令行传入修改参数

  // 输出变量值
  NS_LOG_INFO("运行参数");
  NS_LOG_INFO("  debug=" << debug);
  NS_LOG_INFO("  模拟时间 duration=" << duration);
  NS_LOG_INFO("  输入文件前缀 prefix_file_name=" << prefix_file_name);


  // 设置 Socket 默认参数  which defined in tcp-socket.cc
  //Config::SetDefault ("ns3::TcpSocket::RcvBufSize", UintegerValue (1 << 21));
  //Config::SetDefault ("ns3::TcpSocket::SndBufSize", UintegerValue (1 << 21));
  //Config::SetDefault ("ns3::TcpSocket::InitialCwnd", UintegerValue (1 << 21));
  Config::SetDefault ("ns3::TcpSocket::InitialSlowStartThreshold", UintegerValue (2*1000*1000));


  // Select TCP variant
  if (transport_prot.compare ("TcpNewReno") == 0)
    {
      Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpNewReno::GetTypeId ()));
    }
  else if (transport_prot.compare ("TcpHybla") == 0)
    {
      Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpHybla::GetTypeId ()));
    }
  else if (transport_prot.compare ("TcpHighSpeed") == 0)
    {
      Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpHighSpeed::GetTypeId ()));
    }
  else if (transport_prot.compare ("TcpVegas") == 0)
    {
      Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpVegas::GetTypeId ()));
    }
  else if (transport_prot.compare ("TcpScalable") == 0)
    {
      Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpScalable::GetTypeId ()));
    }
  else if (transport_prot.compare ("TcpHtcp") == 0)
    {
      Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpHtcp::GetTypeId ()));
    }
  else if (transport_prot.compare ("TcpVeno") == 0)
    {
      Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpVeno::GetTypeId ()));
    }
  else if (transport_prot.compare ("TcpBic") == 0)
    {
      Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpBic::GetTypeId ()));
    }
  else if (transport_prot.compare ("TcpYeah") == 0)
    {
      Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpYeah::GetTypeId ()));
    }
  else if (transport_prot.compare ("TcpIllinois") == 0)
    {
      Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpIllinois::GetTypeId ()));
    }
  // #disable TcpMyAlg for common ns3 upstream 
  #if 0
  else if (transport_prot.compare ("TcpMyAlg") == 0) // MyAlg
  {
      Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpMyAlg::GetTypeId ()));
      Config::SetDefault ("ns3::TcpWestwood::FilterType", EnumValue (TcpMyAlg::TUSTIN));
  }
  #endif
  else if (transport_prot.compare ("TcpWestwood") == 0)
    { // the default protocol type in ns3::TcpWestwood is WESTWOOD
      Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpWestwood::GetTypeId ()));
      Config::SetDefault ("ns3::TcpWestwood::FilterType", EnumValue (TcpWestwood::TUSTIN));
    }
  else if (transport_prot.compare ("TcpWestwoodPlus") == 0)
    {
      Config::SetDefault ("ns3::TcpL4Protocol::SocketType", TypeIdValue (TcpWestwood::GetTypeId ()));
      Config::SetDefault ("ns3::TcpWestwood::ProtocolType", EnumValue (TcpWestwood::WESTWOODPLUS));
      Config::SetDefault ("ns3::TcpWestwood::FilterType", EnumValue (TcpWestwood::TUSTIN));
    }
  else
    {
      NS_LOG_DEBUG ("Invalid TCP version");
      exit (1);
    }

  //=========== Calculate parameters based on value of k ===========//
  // Note: the format of host's address is 10.pod.switch.(host+2)
  //
  int num_pod = k;		      // number of pod
  int num_host = (k / 2);		// number of hosts under a switch
  int num_edge = (k / 2);		// number of edge switch in a pod
  int num_bridge = num_edge;// number of bridge in a pod
  int num_agg = (k / 2);		// number of aggregation switch in a pod
  int num_group = k / 2;		// number of group of core switches
  int num_core = (k / 2);		// number of core switch in a group
  int total_host = k * k * k / 4;	// number of hosts in the entire network

  //
  int podRand = 0;	//
  int swRand = 0;		// Random values for servers' address
  int hostRand = 0;	//

  int rand1 = 0;		//
  int rand2 = 0;		// Random values for clients' address
  int rand3 = 0;		//

  // Initialize other variables
  //
  int i = 0;
  int j = 0;
  int h = 0;

  // Output some useful information
  //
  std::cout << ("拓扑参数") << "\n";
  std::cout << "Value of k (ports per switch) =  " << k << "\n";
  std::cout << "Number of Pod (num_pod) = " << num_pod << "\n";
  std::cout << "Total number of hosts (total_host) =  " << total_host << "\n";
  std::cout << "Number of hosts under each switch (num_host) =  " << num_host << "\n";
  std::cout << "Number of edge switch under each pod (num_edge) =  " << num_edge << "\n";
  std::cout << "------------- " << "\n";

  // Initialize Internet Stack and Routing Protocols
  //
  InternetStackHelper internet;
  Ipv4NixVectorHelper nixRouting;
  Ipv4StaticRoutingHelper staticRouting;
  Ipv4ListRoutingHelper list;
  list.Add (staticRouting, 0);
  list.Add (nixRouting, 10);
  internet.SetRoutingHelper (list);

//=========== Creation of Node Containers ===========//
//
  //std::array < Ptr< NodeContainer >, num_group > core{ CreateObject< NodeContainer >() };
  NS_LOG_INFO("生成 Core nodes ");
  NodeContainer core[num_group];	// NodeContainer for core switches
  for (i = 0; i < num_group; i++)
    {
      core[i].Create (num_core);
      internet.Install (core[i]);
      NS_LOG_DEBUG("setup Core switch[i].Get(0) on node id: " << core[i].Get(0)->GetId());
    }
  NodeContainer agg[num_pod];	// NodeContainer for aggregation switches
  for (i = 0; i < num_pod; i++)
    {
      agg[i].Create (num_agg);
      internet.Install (agg[i]);
    }
  NodeContainer edge[num_pod];		// NodeContainer for edge switches
  for (i = 0; i < num_pod; i++)
    {
      edge[i].Create (num_bridge);
      internet.Install (edge[i]);
    }
  NodeContainer bridge[num_pod];	// NodeContainer for edge bridges
  for (i = 0; i < num_pod; i++)
    {
      bridge[i].Create (num_bridge);
      internet.Install (bridge[i]);
    }
  NodeContainer host[num_pod][num_bridge];	// NodeContainer for hosts

  NS_LOG_INFO("生成 Host nodes ");
  for (i = 0; i < k; i++)
    {

      for (j = 0; j < num_bridge; j++)
        {
          host[i][j].Create (num_host);
          internet.Install (host[i][j]);

          if (UdpEchoTestOnly)
            { // setup udp echo servers
              UdpEchoServerHelper echoServer (port);
              // install all echo server
              ApplicationContainer serverApps = echoServer.Install (host[i][j]);
              serverApps.Start (Seconds (1.0));
              serverApps.Stop (Seconds (100.0));
              NS_LOG_INFO(
                  "Setup Echo server on NodeContainer host["<< i <<"]["<< j <<"].Get("<< k <<") at port 9 ");
              NS_LOG_DEBUG("setup UdpEchoServer on node id: " << host[i][j].Get(0)->GetId());
            }
          else
            { // setup tcp sinker
              NS_LOG_DEBUG("setup Tcp Sinker on node id: " << host[i][j].Get(0)->GetId());
              Address bindAddressAndPort (InetSocketAddress (Ipv4Address::GetAny (), port));
              PacketSinkHelper packetSinkHelper ("ns3::TcpSocketFactory", bindAddressAndPort);
              ApplicationContainer hubApp = packetSinkHelper.Install (host[i][j]);
              hubApp.Start (Seconds (start_time));
              hubApp.Stop (Seconds (duration));
            }
        }
    }

//=========== Initialize settings for On/Off Application ===========//
//

// Generate traffics for the simulation
//

  if (num_flows == -1)
    { // 判断是否需要限制 随机流, 减少测试时间
      num_flows = total_host;
    }
  NS_LOG_INFO("生成 "<< num_flows <<" 条随机流进行测试");

  ApplicationContainer app[total_host];
  for (i = 0; i < num_flows; i++) // for (i = 0; i < total_host; i++)
    {
      // Randomly select a server
      podRand = rand () % num_pod + 0;
      swRand = rand () % num_edge + 0;
      hostRand = rand () % num_host + 0;
      hostRand = hostRand + 2;
      char *add;
      add = toString (10, podRand, swRand, hostRand);

      // Initialize On/Off Application with addresss of server
      OnOffHelper oo = OnOffHelper ("ns3::TcpSocketFactory",
                                    Address (InetSocketAddress (Ipv4Address (add), port))); // ip address of server
      //ns-3.13-API
      // oo.SetAttribute("OnTime",RandomVariableValue(ExponentialVariable(1)));
      // oo.SetAttribute("OffTime",RandomVariableValue(ExponentialVariable(1)));

      //ns-3.26-API

      //oo.SetAttribute ("OnTime", StringValue ("ns3::ConstantRandomVariable[Constant=1000]"));
      //oo.SetAttribute ("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=0]"));
      oo.SetAttribute ("OnTime", StringValue ("ns3::ExponentialRandomVariable[Mean=1|Bound=0.0]"));
      oo.SetAttribute ("OffTime", StringValue ("ns3::ExponentialRandomVariable[Mean=1|Bound=0.0]"));

      oo.SetAttribute ("PacketSize", UintegerValue (packetSize));
      oo.SetAttribute ("DataRate", StringValue (dataRate_OnOff));
      oo.SetAttribute ("MaxBytes", StringValue (maxBytes));

      // Randomly select a client
      rand1 = rand () % num_pod + 0;
      rand2 = rand () % num_edge + 0;
      rand3 = rand () % num_host + 0;
      while (rand1 == podRand && swRand == rand2 && (rand3 + 2) == hostRand)
        {
          rand1 = rand () % num_pod + 0;
          rand2 = rand () % num_edge + 0;
          rand3 = rand () % num_host + 0;
        } // to make sure that client and server are different

      // Install On/Off Application to the client
      Ptr<Node> node = host[rand1][rand2].Get (rand3);

      if (UdpEchoTestOnly)
        { // if echo test only, disable random packets; 使用后面的顺序测试
          // app[i].Start (Seconds (i+2.0));
          // app[i].Stop (Seconds (i+2.1));
        }
      else
        { // full duration test;
          app[i] = oo.Install (node);
          app[i].Start (Seconds (start_time)); // 客户端比服务端启动晚 0.001
          if (debug)
            app[i].Stop (Seconds (start_time+1)); // debug 模式下, 只运行很短的流量测试
          else
            app[i].Stop (Seconds (duration));

        }
      NS_LOG_DEBUG(
          "install app [" << i << "] OnOff on node id:" << node->GetId() << " host ["<< rand1 <<"]["<< rand2 <<"].Get("<<rand3 <<") connect to "<< add);
      NODE_ID = node->GetId (); // save node id for tracing
    }

  // UdpEcho顺序测试
  if (UdpEchoTestOnly)
    {
      // k= 4;  host[0][0].Get(0) 10.0.0.2 Get(1) 10.0.0.3
      int seq = 0;
      for (i = 0; i < num_pod; i++)
        {
          for (j = 0; j < num_host; j++)
            {
              seq++;
              char *add;
              add = toString (10, i, 1, 2 + j);
              NS_LOG_INFO("Setup Echo Client( connet -> 9) at address " << add);
              UdpEchoClientHelper echoClient (Ipv4Address (add), port); // 目标地址与端口
              echoClient.SetAttribute ("MaxPackets", UintegerValue (1));
              echoClient.SetAttribute ("Interval", TimeValue (Seconds (1.)));
              echoClient.SetAttribute ("PacketSize", UintegerValue (1024));
              ApplicationContainer clientApp = echoClient.Install (host[0][0].Get (0));
              clientApp.Start (Seconds (seq * 2)); // start one app every 2 seconds
              clientApp.Stop (Seconds (seq * 2 + 20.0));
            }
        }
    }
  else
    {
#if 0
      // 准确(非随机)定义一个Onoff 客户端 (10.0.0.2) 发往 10.3.1.3
      char *add;
      add = toString (10, 3, 1, 3);
      NS_LOG_INFO("Setup OnOff client (connet -> 9), address " << add );
      OnOffHelper onOffHelper ("ns3::TcpSocketFactory", Address ());
      onOffHelper.SetAttribute ("OnTime", StringValue ("ns3::ConstantRandomVariable[Constant=1]"));
      onOffHelper.SetAttribute ("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=0]"));
      AddressValue remoteAddress (InetSocketAddress (Ipv4Address(add) , port));
      onOffHelper.SetAttribute ("Remote", remoteAddress);
      ApplicationContainer clientApps3 = onOffHelper.Install (host[0][0].Get(0));
      clientApps3.Start (Seconds (5.0));
      clientApps3.Stop (Seconds (5.03));// 发2个包 , 每 0.1
#endif
    }

  std::cout << "Finished creating On/Off traffic" << "\n";

// Inintialize Address Helper
//
  Ipv4AddressHelper address;

// Initialize PointtoPoint helper
//
  PointToPointHelper p2p;
  p2p.SetDeviceAttribute ("DataRate", StringValue (dataRate));
  p2p.SetChannelAttribute ("Delay", TimeValue (MilliSeconds (delay)));
  // p2p.SetChannelAttribute ("Delay", StringValue (delay));

// Initialize Csma helper
//
  CsmaHelper csma;
  csma.SetChannelAttribute ("DataRate", StringValue (dataRate));
  csma.SetChannelAttribute ("Delay", TimeValue (MilliSeconds (delay)));
  //csma.SetChannelAttribute ("Delay", StringValue (delay));

//=========== Connect edge switches to hosts ===========//
//
  NetDeviceContainer hostSw[num_pod][num_bridge];
  NetDeviceContainer bridgeDevices[num_pod][num_bridge];
  Ipv4InterfaceContainer interfaces[num_pod][num_bridge];

  for (i = 0; i < num_pod; i++)
    {
      for (j = 0; j < num_bridge; j++)
        {
          NetDeviceContainer link1 = csma.Install (
              NodeContainer (edge[i].Get (j), bridge[i].Get (j)));
          hostSw[i][j].Add (link1.Get (0));
          bridgeDevices[i][j].Add (link1.Get (1));

          for (h = 0; h < num_host; h++)
            {
              NetDeviceContainer link2 = csma.Install (
                  NodeContainer (host[i][j].Get (h), bridge[i].Get (j)));
              hostSw[i][j].Add (link2.Get (0));
              bridgeDevices[i][j].Add (link2.Get (1));
            }

          BridgeHelper bHelper;
          bHelper.Install (bridge[i].Get (j), bridgeDevices[i][j]);
          //Assign address
          char *subnet;
          subnet = toString (10, i, j, 0);
          address.SetBase (subnet, "255.255.255.0");
          interfaces[i][j] = address.Assign (hostSw[i][j]);
#if 1 // display ip address topo
          // NS_LOG_DEBUG("  interfaces " << i << " " << j);
          printInterfaceAddress (interfaces[i][j]);
          // NS_LOG_DEBUG("  Finised interface "<< i << "  "<< j <<" "<< toString (10, i, j, 0) << " setup");
#endif
        }
      NS_LOG_DEBUG("--- finised pod "<< i <<" "<< toString (10, i, 0, 0) << " setup ---");
    }
  std::cout << "Finished connecting edge switches and hosts  " << "\n";

//=========== Connect aggregate switches to edge switches ===========//
//
  NetDeviceContainer ae[num_pod][num_agg][num_edge];
  Ipv4InterfaceContainer ipAeContainer[num_pod][num_agg][num_edge];
  for (i = 0; i < num_pod; i++)
    {
      for (j = 0; j < num_agg; j++)
        {
          for (h = 0; h < num_edge; h++)
            {
              ae[i][j][h] = p2p.Install (agg[i].Get (j), edge[i].Get (h));

              int second_octet = i;
              int third_octet = j + (k / 2);
              int fourth_octet;
              if (h == 0)
                fourth_octet = 1;
              else
                fourth_octet = h * 2 + 1;
              //Assign subnet
              char *subnet;
              subnet = toString (10, second_octet, third_octet, 0);
              //Assign base
              char *base;
              base = toString (0, 0, 0, fourth_octet);
              address.SetBase (subnet, "255.255.255.0", base);
              ipAeContainer[i][j][h] = address.Assign (ae[i][j][h]);
            }
        }
    }
  std::cout << "Finished connecting aggregation switches and edge switches  " << "\n";

//=========== Connect core switches to aggregate switches ===========//
//
  NetDeviceContainer ca[num_group][num_core][num_pod];
  Ipv4InterfaceContainer ipCaContainer[num_group][num_core][num_pod];
  int fourth_octet = 1;

  for (i = 0; i < num_group; i++)
    {
      for (j = 0; j < num_core; j++)
        {
          fourth_octet = 1;
          for (h = 0; h < num_pod; h++)
            {
              ca[i][j][h] = p2p.Install (core[i].Get (j), agg[h].Get (i));

              int second_octet = k + i;
              int third_octet = j;
              //Assign subnet
              char *subnet;
              subnet = toString (10, second_octet, third_octet, 0);
              //Assign base
              char *base;
              base = toString (0, 0, 0, fourth_octet);
              address.SetBase (subnet, "255.255.255.0", base);
              ipCaContainer[i][j][h] = address.Assign (ca[i][j][h]);
              fourth_octet += 2;
            }
        }
    }

  std::cout << "Finished connecting core switches and aggregation switches  " << "\n";
  std::cout << "------------- " << "\n";

//=========== Start the simulation ===========//
//

// Set up tracing if enabled
  if (tracing)
    {

      std::ofstream ascii;
      Ptr<OutputStreamWrapper> ascii_wrap;

      prefix_file_name += "-" + transport_prot; // 文件名中增加 tcp类型
      NS_LOG_UNCOND("激活 tracing 文件记录 " << prefix_file_name);

      // enable ascii & pacap full tracing
      if (ascii_trace)
        {
          std::string ascii_trace_filename = prefix_file_name + "-ascii";
          ascii.open (ascii_trace_filename.c_str ());
          ascii_wrap = new OutputStreamWrapper (ascii_trace_filename.c_str (), std::ios::out);
          internet.EnableAsciiIpv4All (ascii_wrap); // 激活 tracing 很容易看到对应的 id 信息
        }
      if (pcap)
        csma.EnablePcapAll (prefix_file_name, false); // 激活 pacap 抓包

      if (debug)
        {
          Config::ConnectWithoutContext ("/NodeList/*/ApplicationList/*/$ns3::PacketSink/Rx",
                                     MakeCallback (&SinkRx));
        }

      Time s_time = Seconds(start_time + 0.00001);
      Simulator::Schedule (s_time, &TraceCwnd, prefix_file_name + "-cwnd.data");
      Simulator::Schedule (s_time, &TraceSsThresh, prefix_file_name + "-ssth.data");
      Simulator::Schedule (s_time, &TraceRtt, prefix_file_name + "-rtt.data");
      Simulator::Schedule (s_time, &TraceRto, prefix_file_name + "-rto.data");
      Simulator::Schedule (s_time, &TraceNextTx, prefix_file_name + "-next-tx.data");
      Simulator::Schedule (s_time, &TraceInFlight, prefix_file_name + "-inflight.data");
      Simulator::Schedule (Seconds (0.1), &TraceNextRx, prefix_file_name + "-next-rx.data");

      //trace qlen; copy from traffic-control.cc
      AsciiTraceHelper asciiTraceHelper;
      qlenStream = asciiTraceHelper.CreateFileStream ((prefix_file_name + "-qlen.data").c_str ());
      //Config::ConnectWithoutContext("/NodeList/0/$ns3::TrafficControlLayer/RootQueueDiscList/0/PacketsInQueue", MakeCallback (&TcPacketsInQueueTrace));
      Config::ConnectWithoutContext("/NodeList/*/DeviceList/*/$ns3::PointToPointNetDevice/TxQueue/PacketsInQueue",MakeCallback (&DevicePacketsInQueueTrace));
    }

  Ipv4GlobalRoutingHelper::PopulateRoutingTables ();
  // ======================================================================
  // Print routing tables at T=0.1
  // ----------------------------------------------------------------------

#if 0
  NS_LOG_INFO ("Set up to print routing tables at T=0.1s");
  Ptr<OutputStreamWrapper> routingStream =
  Create<OutputStreamWrapper> (prefix_file_name + "-router.routes", std::ios::out);
  Ipv4GlobalRoutingHelper g;
  g.PrintRoutingTableAllAt (Seconds (0.1), routingStream);
#endif

	//
	GtkConfigStore configstore;
  configstore.ConfigureAttributes();

  std::cout << "Start Simulation.. " << "\n";


  // Calculate Throughput using Flowmonitor
  //
  FlowMonitorHelper flowmon;
  Ptr<FlowMonitor> monitor;
  if (flow_monitor)
    monitor = flowmon.InstallAll ();

  // Run simulation.
  //
  NS_LOG_INFO("Run Simulation.");
  Simulator::Stop (Seconds (duration + 1));
  Simulator::Run ();

  if (flow_monitor)
    {
      monitor->CheckForLostPackets ();
      monitor->SerializeToXmlFile (prefix_file_name + ".k" + std::to_string (k) + ".xml", true, true);
    }

  std::cout << "Simulation finished " << "\n";

  Simulator::Destroy ();
  NS_LOG_INFO("Done.");

  return 0;
}

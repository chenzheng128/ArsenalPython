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

using namespace ns3;

// 定义日志组件名
NS_LOG_COMPONENT_DEFINE ("FirstScriptExample");

int
main (int argc, char *argv[])
{

  //自定义参数
  // ./waf --run "scratch/myfirst --PrintHelp"  # 显示自定义参数
  // ./waf --run "scratch/myfirst --nPackets=2" # 运行自定义参数
  uint32_t nPackets = 1;

  //增加参数， 日志支持
  CommandLine cmd;
  cmd.AddValue("nPackets", "Number of packets to echo", nPackets);
  cmd.Parse (argc, argv);

  // TODO 会导致错误 msg="Could not set default value for ns3::Ipv4L3Protocol::CalcChecksum", file=../src/core/model/config.cc, line=779
  //Config::SetDefault ("ns3::Ipv4L3Protocol::CalcChecksum", BooleanValue (true));

  //if (nPackets != 1)
      // UNCOND 仅工作在 debug 模式下, Optimazed 是不会输出的
      NS_LOG_UNCOND ("读入自定义 nPackets 参数 = " << nPackets);

  NS_LOG_INFO ("Creating Topology two nodes ");

  Time::SetResolution (Time::NS);
  // 设置 level 级别 $ export NS_LOG=UdpEchoClientApplication=level_all
  // export NS_LOG=UdpEchoClientApplication=level_debug
  LogComponentEnable ("UdpEchoClientApplication", LOG_LEVEL_INFO);
  LogComponentEnable ("UdpEchoServerApplication", LOG_LEVEL_INFO);

  // 需要用下面两种方法之一激活日志组件, 才能看到后面的 NS_LOG_INFO () 输出
  // export NS_LOG=FirstScriptExample=info
  LogComponentEnable ("FirstScriptExample", LOG_LEVEL_INFO);

  NodeContainer nodes;
  nodes.Create (2);
  NS_LOG_INFO ("创建 2 个节点的拓扑 Creating Topology");

  PointToPointHelper pointToPoint;
  pointToPoint.SetDeviceAttribute ("DataRate", StringValue ("5Mbps"));
  pointToPoint.SetChannelAttribute ("Delay", StringValue ("2ms"));

  NetDeviceContainer devices;
  devices = pointToPoint.Install (nodes);

  InternetStackHelper stack;
  stack.Install (nodes);

  Ipv4AddressHelper address;
  address.SetBase ("10.1.1.0", "255.255.255.0");

  Ipv4InterfaceContainer interfaces = address.Assign (devices);

  UdpEchoServerHelper echoServer (9);

  ApplicationContainer serverApps = echoServer.Install (nodes.Get (1));
  serverApps.Start (Seconds (1.0));
  serverApps.Stop (Seconds (20.0));

  UdpEchoClientHelper echoClient (interfaces.GetAddress (1), 9);
  echoClient.SetAttribute ("MaxPackets", UintegerValue (nPackets));
  echoClient.SetAttribute ("Interval", TimeValue (Seconds (1.0)));
  echoClient.SetAttribute ("PacketSize", UintegerValue (1024));

  ApplicationContainer clientApps = echoClient.Install (nodes.Get (0));
  clientApps.Start (Seconds (5.0));
  clientApps.Stop (Seconds (20.0));

  //生成 ascii Tracing
  AsciiTraceHelper ascii;
  pointToPoint.EnableAsciiAll (ascii.CreateFileStream ("myfirst.tr"));
  //生成 pcap
  // tcpdump -nn -tt -r myfirst-0-0.pcap # 查看 pcap
  pointToPoint.EnablePcapAll ("myfirst");

  Simulator::Run ();
  Simulator::Destroy ();
  return 0;
}

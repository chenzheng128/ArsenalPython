// Random settings examples
// Authors: Zheng Chen

/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */

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
#include "ns3/random-variable-stream.h"

using namespace ns3;
using namespace std;
NS_LOG_COMPONENT_DEFINE ("CUC-Random-Var");

int main(){
  // init ExponentialRandomVariable method1
  double mean = 1;
  double bound = 0.0;
  Ptr<ExponentialRandomVariable> ev = CreateObject<ExponentialRandomVariable> ();
  ev->SetAttribute ("Mean", DoubleValue (mean));
  ev->SetAttribute ("Bound", DoubleValue (bound));
  cout << "ExponentialRandomVariable: " << ev->GetValue() << endl;

  // setting value method2
  cout << (StringValue ("ns3::ExponentialRandomVariable[Mean=1|Bound=0.0]")).Get() << endl ;

}

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

#include "ns3/core-module.h" // 加入日志处理
#include "ns3/object.h"
#include "ns3/uinteger.h"
#include "ns3/traced-value.h"
#include "ns3/trace-source-accessor.h"

#include <iostream>

using namespace ns3;

// 定义日志组件名
NS_LOG_COMPONENT_DEFINE ("FourthScriptExample");

class MyObject : public Object
{
public:
  /**
   * Register this type.
   * \return The TypeId.
   */
  static TypeId GetTypeId (void)
  {
    static TypeId tid = TypeId ("MyObject")
      .SetParent<Object> ()
      .SetGroupName ("Tutorial")
      .AddConstructor<MyObject> ()
      .AddTraceSource ("MyInteger",  //定义了 MyInteger 标示，并将其关联至 m_myInt
                       "An integer value to trace.",
                       MakeTraceSourceAccessor (&MyObject::m_myInt),
                       "ns3::TracedValueCallback::Int32")
    ;
    return tid;
  }

  MyObject () {}
  TracedValue<int32_t> m_myInt;  //我们要跟踪的对象
};

//定义了 Callback 函数
void
IntTrace (int32_t oldValue, int32_t newValue)
{
  std::cout << "Traced myObject m_myInt:  " << oldValue << " to " << newValue << std::endl;
}

// 映射关系为 m_myInt -> MyInteger -> IntTrace()
int
main (int argc, char *argv[])
{
  Ptr<MyObject> myObject = CreateObject<MyObject> ();

  // Trace 连接 TraceSource， 将 MyInteger 标示 和 IntTrace Callback 回调函数进行关联
  NS_LOG_UNCOND( "// Trace 连接 TraceSource:  映射关系为 m_myInt -> MyInteger -> IntTrace()");
  myObject->TraceConnectWithoutContext ("MyInteger", MakeCallback (&IntTrace));

  // sink 触发了事件改变
  myObject->m_myInt = 1234;

  //再次触发事件
  myObject->m_myInt = 512;

  NS_LOG_UNCOND( "// Trace 断开， 断开之后 不再显示 m_myInt 改变");
  myObject->TraceDisconnectWithoutContext("MyInteger", MakeCallback (&IntTrace));
  // 不再触发
  myObject->m_myInt = 254;
}

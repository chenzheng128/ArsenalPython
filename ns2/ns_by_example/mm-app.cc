//  
// Author:    Jae Chung  
// File:      mm-app.cc
// Written:   07/17/99 (for ns-2.1b4a)  
// Modifed:   10/14/01 (for ns-2.1b8a)  
//   

#include "random.h"
#include "mm-app.h"


// MmApp OTcl linkage class
static class MmAppClass : public TclClass {
 public:
  MmAppClass() : TclClass("Application/MmApp") {}
  TclObject* create(int, const char*const*) {
    return (new MmApp);
  }
} class_app_mm;


// When snd_timer_ expires call MmApp:send_mm_pkt()
void SendTimer::expire(Event*)
{
  t_->send_mm_pkt();
}


// When ack_timer_ expires call MmApp:send_ack_pkt()
void AckTimer::expire(Event*)
{
  t_->send_ack_pkt();
}


// Constructor (also initialize instances of timers)
MmApp::MmApp() : running_(0), snd_timer_(this), ack_timer_(this)
{
  bind_bw("rate0_", &rate[0]);
  bind_bw("rate1_", &rate[1]);
  bind_bw("rate2_", &rate[2]);
  bind_bw("rate3_", &rate[3]);
  bind_bw("rate4_", &rate[4]);
  bind("pktsize_", &pktsize_);
  bind_bool("random_", &random_);
}


// OTcl command interpreter
int MmApp::command(int argc, const char*const* argv)
{
  Tcl& tcl = Tcl::instance();

  if (argc == 3) {
    if (strcmp(argv[1], "attach-agent") == 0) {
      agent_ = (Agent*) TclObject::lookup(argv[2]);
      if (agent_ == 0) {
	tcl.resultf("no such agent %s", argv[2]);
	return(TCL_ERROR);
      }

      // Make sure the underlying agent support MM
      if(agent_->supportMM()) {
	agent_->enableMM();
      }
      else {
	tcl.resultf("agent \"%s\" does not support MM Application", argv[2]);
	return(TCL_ERROR);
      }
      
      agent_->attachApp(this);
      return(TCL_OK);
    }
  }
  return (Application::command(argc, argv));
}



void MmApp::init()
{
  scale_ = 0; // Start at minimum rate
  seq_ = 0;   // MM sequence number (start from 0)
  interval_ = (double)(pktsize_ << 3)/(double)rate[scale_];
}


void MmApp::start()
{
  init();
  running_ = 1;
  send_mm_pkt();
}


void MmApp::stop()
{
  running_ = 0;
}


// Send application data packet
void MmApp::send_mm_pkt()
{
  hdr_mm mh_buf;

  if (running_) {
    // the below info is passed to UDPmm agent, which will write it 
    // to MM header after packet creation.
    mh_buf.ack = 0;            // This is a MM packet
    mh_buf.seq = seq_++;         // MM sequece number
    mh_buf.nbytes = pktsize_;  // Size of MM packet (NOT UDP packet size)
    mh_buf.time = Scheduler::instance().clock(); // Current time
    mh_buf.scale = scale_;                       // Current scale value
    agent_->sendmsg(pktsize_, (char*) &mh_buf);  // send to UDP

    // Reschedule the send_pkt timer
    double next_time_ = next_snd_time();
    if(next_time_ > 0) snd_timer_.resched(next_time_);
  }
}


// Schedule next data packet transmission time
double MmApp::next_snd_time()
{
  // Recompute interval in case rate or size chages
  interval_ = (double)(pktsize_ << 3)/(double)rate[scale_];
  double next_time_ = interval_;
  if(random_) 
    next_time_ += interval_ * Random::uniform(-0.5, 0.5);
  return next_time_;
}


// Receive message from underlying agent
void MmApp::recv_msg(int nbytes, const char *msg)
{
  if(msg) {
    hdr_mm* mh_buf = (hdr_mm*) msg;

    if(mh_buf->ack == 1) {
      // If received packet is ACK packet
      set_scale(mh_buf);
    }
    else {
      // If received packet is MM packet
      account_recv_pkt(mh_buf);
      if(mh_buf->seq == 0) send_ack_pkt();
    }
  }
}


// Sender sets its scale to what reciver notifies
void MmApp::set_scale(const hdr_mm *mh_buf)
{ 
  scale_ = mh_buf->scale;
}


void MmApp::account_recv_pkt(const hdr_mm *mh_buf)
{ 
  double local_time = Scheduler::instance().clock();

  // Calculate RTT
  if(mh_buf->seq == 0) {
    init_recv_pkt_accounting();
    p_accnt.rtt = 2*(local_time - mh_buf->time);
  }
  else
    p_accnt.rtt = 0.9 * p_accnt.rtt + 0.1 * 2*(local_time - mh_buf->time); 

  // Count Received packets and Calculate Packet Loss
  p_accnt.recv_pkts ++;
  p_accnt.lost_pkts += (mh_buf->seq - p_accnt.last_seq - 1);
  p_accnt.last_seq = mh_buf->seq;
}


void MmApp::init_recv_pkt_accounting()
{
  p_accnt.last_seq = -1;
  p_accnt.last_scale = 0; 
  p_accnt.lost_pkts = 0;
  p_accnt.recv_pkts = 0;
}


void MmApp::send_ack_pkt(void)
{
  double local_time = Scheduler::instance().clock();

  adjust_scale();

  // send ack message
  hdr_mm ack_buf;
  ack_buf.ack = 1;  // this packet is ack packet
  ack_buf.time = local_time;
  ack_buf.nbytes = 40;  // Ack packet size is 40 Bytes
  ack_buf.scale = p_accnt.last_scale;
  agent_->sendmsg(ack_buf.nbytes, (char*) &ack_buf);

  // schedul next ACK time
  ack_timer_.resched(p_accnt.rtt);
}


void MmApp::adjust_scale(void)
{
  if(p_accnt.recv_pkts > 0) {
    if(p_accnt.lost_pkts > 0)
      p_accnt.last_scale = (int)(p_accnt.last_scale / 2);
    else {
      p_accnt.last_scale++;
      if(p_accnt.last_scale > 4) p_accnt.last_scale = 4;
    }
  }
  p_accnt.recv_pkts = 0;
  p_accnt.lost_pkts = 0;
}

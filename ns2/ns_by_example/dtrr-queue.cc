//
// Author:    Jae Chung
// File:      dtrr-queue.cc
// Written:   07/19/99 (for ns-2.1b4a)
// Modifed:   10/14/01 (for ns-2.1b8a)
// 

#include "dtrr-queue.h"

static class DtRrQueueClass : public TclClass {
public:
        DtRrQueueClass() : TclClass("Queue/DTRR") {}
        TclObject* create(int, const char*const*) {
	         return (new DtRrQueue);
	}
} class_dropt_tail_round_robin;


void DtRrQueue::enque(Packet* p)
{
  hdr_ip* iph = hdr_ip::access(p);
  
  // if IPv6 priority = 15 enqueue to queue1
  if (iph->prio_ == 15) {
    q1_->enque(p);
    if ((q1_->length() + q2_->length()) > qlim_) {
      q1_->remove(p);
      drop(p);
    }
  }
  else {
    q2_->enque(p);
    if ((q1_->length() + q2_->length()) > qlim_) {
      q2_->remove(p);
      drop(p);
    }
  }
}


Packet* DtRrQueue::deque()
{
  Packet *p;
  
  if (deq_turn_ == 1) {
    p =  q1_->deque();
    if (p == 0) {
      p = q2_->deque();
      deq_turn_ = 1;
    }
    else {
      deq_turn_ = 2;
    }
  }
  else {
    p =  q2_->deque();
    if (p == 0) {
      p = q1_->deque();
      deq_turn_ = 2;
    }
    else {
      deq_turn_ = 1;
    }
  }
  
  return (p);
}







//
// Author:    Jae Chung
// File:      dtrr-queue.h
// Written:   07/19/99 (for ns-2.1b4a)
// Modifed:   10/14/01 (for ns-2.1b8a)
//

#include <string.h>
#include "queue.h"
#include "address.h"


class DtRrQueue : public Queue {
 public:
         DtRrQueue() { 
		q1_ = new PacketQueue;
		q2_ = new PacketQueue;
		pq_ = q1_;
		deq_turn_ = 1;
	}

 protected:
         void enque(Packet*);
	 Packet* deque();

	 PacketQueue *q1_;   // First  FIFO queue
	 PacketQueue *q2_;   // Second FIFO queue
	 int deq_turn_;      // 1 for First queue 2 for Second
};

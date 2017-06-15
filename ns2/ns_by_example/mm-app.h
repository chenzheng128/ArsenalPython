//
// Author:    Jae Chung
// File:      mm-app.h
// Written:   07/17/99 (for ns-2.1b4a)
// Modifed:   10/14/01 (for ns-2.1b8a)
// 

#include "timer-handler.h"
#include "packet.h"
#include "app.h"
#include "udp-mm.h"

// This is used for receiver's received packet accounting
struct pkt_accounting { 
        int last_seq;   // sequence number of last received MM pkt
        int last_scale; // rate (0-4) of last acked
        int lost_pkts;  // number of lost pkts since last ack
        int recv_pkts;  // number of received pkts since last ack
        double rtt;     // round trip time
};


class MmApp;


// Sender uses this timer to 
// schedule next app data packet transmission time
class SendTimer : public TimerHandler {
 public:
	SendTimer(MmApp* t) : TimerHandler(), t_(t) {}
	inline virtual void expire(Event*);
 protected:
	MmApp* t_;
};


// Reciver uses this timer to schedule
// next ack packet transmission time
class AckTimer : public TimerHandler {
 public:
	AckTimer(MmApp* t) : TimerHandler(), t_(t) {}
	inline virtual void expire(Event*);
 protected:
	MmApp* t_;
};


// Mulitmedia Application Class Definition
class MmApp : public Application {
 public:
	MmApp();
	void send_mm_pkt();  // called by SendTimer:expire (Sender)
	void send_ack_pkt(); // called by AckTimer:expire (Receiver)
 protected:
	int command(int argc, const char*const* argv);
	void start();       // Start sending data packets (Sender)
	void stop();        // Stop sending data packets (Sender)
 private:
	void init();
	inline double next_snd_time();                          // (Sender)
	virtual void recv_msg(int nbytes, const char *msg = 0); // (Sender/Receiver)
	void set_scale(const hdr_mm *mh_buf);                   // (Sender)
	void adjust_scale(void);                                // (Receiver)
	void account_recv_pkt(const hdr_mm *mh_buf);            // (Receiver)
	void init_recv_pkt_accounting();                        // (Receiver)

	double rate[5];        // Transmission rates associated to scale values
	double interval_;      // Application data packet transmission interval
	int pktsize_;          // Application data packet size
	int random_;           // If 1 add randomness to the interval
	int running_;          // If 1 application is running
	int seq_;              // Application data packet sequence number
	int scale_;            // Media scale parameter
	pkt_accounting p_accnt;
	SendTimer snd_timer_;  // SendTimer
	AckTimer  ack_timer_;  // AckTimer
};




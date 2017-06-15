//
// Author:    Jae Chung
// File:      udp-mm.h 
// Written:   07/17/99 (for ns-2.1b4a)
// Modifed:   10/14/01 (for ns-2.1b8a)
// 

#ifndef ns_udp_mm_h
#define ns_udp_mm_h

#include "udp.h"
#include "ip.h"

// Multimedia Header Structure
struct hdr_mm {
	int ack;     // is it ack packet?
	int seq;     // mm sequence number
	int nbytes;  // bytes for mm pkt
	double time; // current time
	int scale;   // scale (0-4) associated with data rates

	// Packet header access functions
        static int offset_;
        inline static int& offset() { return offset_; }
        inline static hdr_mm* access(const Packet* p) {
                return (hdr_mm*) p->access(offset_);
        }
};


// Used for Re-assemble segmented (by UDP) MM packet
struct asm_mm { 
	int seq;     // mm sequence number
	int rbytes;  // currently received bytes
	int tbytes;  // total bytes to receive for MM packet
};


// UdpMmAgent Class definition
class UdpMmAgent : public UdpAgent {
public:
	UdpMmAgent();
	UdpMmAgent(packet_t);
	virtual int supportMM() { return 1; }
	virtual void enableMM() { support_mm_ = 1; }
	virtual void sendmsg(int nbytes, const char *flags = 0);
	void recv(Packet*, Handler*);
protected:
	int support_mm_; // set to 1 if above is MmApp
private:
	asm_mm asm_info; // packet re-assembly information
};

#endif

//
// Author:    Jae Chung
// File:      udp-mm.cc
// Written:   07/17/99 (for ns-2.1b4a)
// Modifed:   10/14/01 (for ns-2.1b8a)
//

#include "udp-mm.h"
#include "rtp.h"
#include "random.h"
#include <string.h>


int hdr_mm::offset_;

// Mulitmedia Header Class 
static class MultimediaHeaderClass : public PacketHeaderClass {
public:
	MultimediaHeaderClass() : PacketHeaderClass("PacketHeader/Multimedia",
						    sizeof(hdr_mm)) {
		bind_offset(&hdr_mm::offset_);
	}
} class_mmhdr;


// UdpMmAgent OTcl linkage class
static class UdpMmAgentClass : public TclClass {
public:
	UdpMmAgentClass() : TclClass("Agent/UDP/UDPmm") {}
	TclObject* create(int, const char*const*) {
		return (new UdpMmAgent());
	}
} class_udpmm_agent;


// Constructor (with no arg)
UdpMmAgent::UdpMmAgent() : UdpAgent()
{
	support_mm_ = 0;
	asm_info.seq = -1;
}

UdpMmAgent::UdpMmAgent(packet_t type) : UdpAgent(type)
{
	support_mm_ = 0;
	asm_info.seq = -1;
}


// Add Support of Multimedia Application to UdpAgent::sendmsg
void UdpMmAgent::sendmsg(int nbytes, const char* flags)
{
	Packet *p;
	int n, remain;

 
	if (size_) {
		n = (nbytes/size_ + (nbytes%size_ ? 1 : 0));
		remain = nbytes%size_;
	}
	else
		printf("Error: UDPmm size = 0\n");

	if (nbytes == -1) {
		printf("Error:  sendmsg() for UDPmm should not be -1\n");
		return;
	}
	double local_time =Scheduler::instance().clock();
	while (n-- > 0) {
		p = allocpkt();
		if(n==0 && remain>0) hdr_cmn::access(p)->size() = remain;
		else hdr_cmn::access(p)->size() = size_;
		hdr_rtp* rh = hdr_rtp::access(p);
		rh->flags() = 0;
		rh->seqno() = ++seqno_;
		hdr_cmn::access(p)->timestamp() = 
		    (u_int32_t)(SAMPLERATE*local_time);
		// to eliminate recv to use MM fields for non MM packets
		hdr_mm* mh = hdr_mm::access(p);
		mh->ack = 0;
		mh->seq = 0;
		mh->nbytes = 0;
		mh->time = 0;
		mh->scale = 0;
		// mm udp packets are distinguished by setting the ip
		// priority bit to 15 (Max Priority).
		if(support_mm_) {
			hdr_ip* ih = hdr_ip::access(p);
			ih->prio_ = 15;
			if(flags) // MM Seq Num is passed as flags
				memcpy(mh, flags, sizeof(hdr_mm));
		}
		// add "beginning of talkspurt" labels (tcl/ex/test-rcvr.tcl)
		if (flags && (0 ==strcmp(flags, "NEW_BURST")))
			rh->flags() |= RTP_M;
		target_->recv(p);
	}
	idle();
}


// Support Packet Re-Assembly and Multimedia Application
void UdpMmAgent::recv(Packet* p, Handler*)
{
	hdr_ip* ih = hdr_ip::access(p);
	int bytes_to_deliver = hdr_cmn::access(p)->size();

	// if it is a MM packet (data or ack)
	if(ih->prio_ == 15) { 
		if(app_) {  // if MM Application exists
			// re-assemble MM Application packet if segmented
			hdr_mm* mh = hdr_mm::access(p);
			if(mh->seq == asm_info.seq)
				asm_info.rbytes += hdr_cmn::access(p)->size();
			else {
				asm_info.seq = mh->seq;
				asm_info.tbytes = mh->nbytes;
				asm_info.rbytes = hdr_cmn::access(p)->size();
			}
			// if fully reassembled, pass the packet to application
			if(asm_info.tbytes == asm_info.rbytes) {
				hdr_mm mh_buf;
				memcpy(&mh_buf, mh, sizeof(hdr_mm));
				app_->recv_msg(mh_buf.nbytes, (char*) &mh_buf);
			}
		}
		Packet::free(p);
	}
	// if it is a normal data packet (not MM data or ack packet)
	else { 
		if (app_) app_->recv(bytes_to_deliver);
		Packet::free(p);
	}
}


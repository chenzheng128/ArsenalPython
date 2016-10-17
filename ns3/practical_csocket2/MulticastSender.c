#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <netdb.h>
#include "Practical.h"

int main(int argc, char *argv[]) {

  if (argc < 4 || argc > 5) // Test for number of parameters
    DieWithUserMessage("Parameter(s)",
		       "<Multicast Address> <Port> <Send String> [<TTL>]");

  char *multicastIPString = argv[1];   // First arg:  multicast IP address
  char *service = argv[2];             // Second arg:  multicast port/service
  char *sendString = argv[3];          // Third arg:  string to multicast

  size_t sendStringLen = strlen(sendString);
  if (sendStringLen > MAXSTRINGLENGTH)        // Check input length
    DieWithUserMessage("String too long", sendString);

  // Fourth arg (optional):  TTL for transmitting multicast packets
  int multicastTTL = (argc == 5) ? atoi(argv[4]) : 1;

  // Tell the system what kind(s) of address info we want
  struct addrinfo addrCriteria;                   // Criteria for address match
  memset(&addrCriteria, 0, sizeof(addrCriteria)); // Zero out structure
  addrCriteria.ai_family = AF_UNSPEC;             // v4 or v6 is OK
  addrCriteria.ai_socktype = SOCK_DGRAM;          // Only datagram sockets
  addrCriteria.ai_protocol = IPPROTO_UDP;         // Only UDP please
  addrCriteria.ai_flags |= AI_NUMERICHOST;        // Don't try to resolve address

  struct addrinfo *multicastAddr;   // Holder for returned address
  int rtnVal= getaddrinfo(multicastIPString, service,
			  &addrCriteria, &multicastAddr);
  if (rtnVal != 0)
    DieWithUserMessage("getaddrinfo() failed", gai_strerror(rtnVal));

  // Create socket for sending datagrams
  int sock = socket(multicastAddr->ai_family, multicastAddr->ai_socktype,
		    multicastAddr->ai_protocol);
  if (sock < 0)
    DieWithSystemMessage("socket() failed");

  // Set TTL of multicast packet. Unfortunately this requires
  // address-family-specific code
  if (multicastAddr->ai_family == AF_INET6) { // v6-specific
    // The v6 multicast TTL socket option requires that the value be
    // passed in as an integer
    if (setsockopt(sock, IPPROTO_IPV6, IPV6_MULTICAST_HOPS,
		   &multicastTTL, sizeof(multicastTTL)) < 0)
      DieWithSystemMessage("setsockopt(IPV6_MULTICAST_HOPS) failed");
  } else if (multicastAddr->ai_family == AF_INET) { // v4 specific
    // The v4 multicast TTL socket option requires that the value be
    // passed in an unsigned char
    u_char mcTTL = (u_char) multicastTTL;
    if (setsockopt(sock, IPPROTO_IP, IP_MULTICAST_TTL, &mcTTL,
		   sizeof(mcTTL)) < 0)
      DieWithSystemMessage("setsockopt(IP_MULTICAST_TTL) failed");
  } else {
    DieWithUserMessage("Unable to set TTL", "invalid address family");
  }

  for (;;) { // Run forever
    // Multicast the string to all who have joined the group
    ssize_t numBytes = sendto(sock, sendString, sendStringLen, 0,
			    multicastAddr->ai_addr, multicastAddr->ai_addrlen);
    if (numBytes < 0)
      DieWithSystemMessage("sendto() failed");
    else if (numBytes != sendStringLen)
      DieWithUserMessage("sendto()", "sent unexpected number of bytes");
    sleep(3);
  }
  // NOT REACHED
}

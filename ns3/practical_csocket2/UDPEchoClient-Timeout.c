#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <signal.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#include "Practical.h"

static const unsigned int TIMEOUT_SECS = 2; // Seconds between retransmits
static const unsigned int MAXTRIES = 5;     // Tries before giving up

unsigned int tries = 0; // Count of times sent - GLOBAL for signal-handler access

void CatchAlarm(int ignored); // Handler for SIGALRM

int main(int argc, char *argv[]) {

  if ((argc < 3) || (argc > 4)) // Test for correct number of arguments
    DieWithUserMessage("Parameter(s)",
        "<Server Address/Name> <Echo Word> [<Server Port/Service>]\n");

  char *server = argv[1];     // First arg: server address/name
  char *echoString = argv[2]; // Second arg: word to echo

  size_t echoStringLen = strlen(echoString);
  if (echoStringLen > MAXSTRINGLENGTH)
    DieWithUserMessage(echoString, "too long");

  char *service = (argc == 4) ? argv[3] : "echo";

  // Tell the system what kind(s) of address info we want
  struct addrinfo addrCriteria;                   // Criteria for address
  memset(&addrCriteria, 0, sizeof(addrCriteria)); // Zero out structure
  addrCriteria.ai_family = AF_UNSPEC;             // Any address family
  addrCriteria.ai_socktype = SOCK_DGRAM;          // Only datagram sockets
  addrCriteria.ai_protocol = IPPROTO_UDP;         // Only UDP protocol

  // Get address(es)
  struct addrinfo *servAddr; // Holder for returned list of server addrs
  int rtnVal = getaddrinfo(server, service, &addrCriteria, &servAddr);
  if (rtnVal != 0)
    DieWithUserMessage("getaddrinfo() failed", gai_strerror(rtnVal));

  // Create a reliable, stream socket using UDP
  int sock = socket(servAddr->ai_family, servAddr->ai_socktype,
      servAddr->ai_protocol); // Socket descriptor for client
  if (sock < 0)
    DieWithSystemMessage("socket() failed");

  // Set signal handler for alarm signal
  struct sigaction handler; // Signal handler
  handler.sa_handler = CatchAlarm;
  if (sigfillset(&handler.sa_mask) < 0) // Block everything in handler
    DieWithSystemMessage("sigfillset() failed");
  handler.sa_flags = 0;

  if (sigaction(SIGALRM, &handler, 0) < 0)
    DieWithSystemMessage("sigaction() failed for SIGALRM");

  // Send the string to the server
  ssize_t numBytes = sendto(sock, echoString, echoStringLen, 0,
      servAddr->ai_addr, servAddr->ai_addrlen);
  if (numBytes < 0)
    DieWithSystemMessage("sendto() failed");
  else if (numBytes != echoStringLen)
    DieWithUserMessage("sendto() error", "sent unexpected number of bytes");

  // Receive a response

  struct sockaddr_storage fromAddr; // Source address of server
  // Set length of from address structure (in-out parameter)
  socklen_t fromAddrLen = sizeof(fromAddr);
  alarm(TIMEOUT_SECS); // Set the timeout
  char buffer[MAXSTRINGLENGTH + 1]; // I/O buffer
  while ((numBytes = recvfrom(sock, buffer, MAXSTRINGLENGTH, 0,
      (struct sockaddr *) &fromAddr, &fromAddrLen)) < 0) {
    if (errno == EINTR) {     // Alarm went off
      if (tries < MAXTRIES) { // Incremented by signal handler
        numBytes = sendto(sock, echoString, echoStringLen, 0,
            (struct sockaddr *) servAddr->ai_addr, servAddr->ai_addrlen);
        if (numBytes < 0)
          DieWithSystemMessage("sendto() failed");
        else if (numBytes != echoStringLen)
          DieWithUserMessage("sendto() error", "sent unexpected number of bytes");
      } else
        DieWithUserMessage("No Response", "unable to communicate with server");
    } else
      DieWithSystemMessage("recvfrom() failed");
  }

  // recvfrom() got something -- cancel the timeout
  alarm(0);

  buffer[echoStringLen] = '\0';     // Null-terminate the received data
  printf("Received: %s\n", buffer); // Print the received data

  close(sock);
  exit(0);
}

// Handler for SIGALRM
void CatchAlarm(int ignored) {
  tries += 1;
}


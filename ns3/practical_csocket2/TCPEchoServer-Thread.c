#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include "Practical.h"

void *ThreadMain(void *arg); // Main program of a thread

// Structure of arguments to pass to client thread
struct ThreadArgs {
  int clntSock; // Socket descriptor for client
};

int main(int argc, char *argv[]) {

  if (argc != 2) // Test for correct number of arguments
    DieWithUserMessage("Parameter(s)", "<Server Port/Service>");

  char *servPort = argv[1]; // First arg:  local port
  int servSock = SetupTCPServerSocket(servPort);
  if (servSock < 0)
    DieWithUserMessage("SetupTCPServerSocket() failed", "unable to establish");
  for (;;) { // Run forever
    int clntSock = AcceptTCPConnection(servSock);

    // Create separate memory for client argument
    struct ThreadArgs *threadArgs = (struct ThreadArgs *) malloc(
        sizeof(struct ThreadArgs));
    if (threadArgs == NULL)
      DieWithSystemMessage("malloc() failed");
    threadArgs->clntSock = clntSock;

    // Create client thread
    pthread_t threadID;
    int returnValue = pthread_create(&threadID, NULL, ThreadMain, threadArgs);
    if (returnValue != 0)
      DieWithUserMessage("pthread_create() failed", strerror(returnValue));
    printf("with thread %ld\n", (long int) threadID);
  }
  // NOT REACHED
}

void *ThreadMain(void *threadArgs) {
  // Guarantees that thread resources are deallocated upon return
  pthread_detach(pthread_self());

  // Extract socket file descriptor from argument
  int clntSock = ((struct ThreadArgs *) threadArgs)->clntSock;
  free(threadArgs); // Deallocate memory for argument

  HandleTCPClient(clntSock);

  return (NULL);
}

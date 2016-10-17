#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include "Practical.h"

void ProcessMain(int servSock); // Process main

int main(int argc, char *argv[]) {

  if (argc != 3) // Test for correct number of arguments
    DieWithUserMessage("Parameter(s)", "<Server Port/Service> <Process Count>");

  char *service = argv[1];                   // First arg:  local port
  unsigned int processLimit = atoi(argv[2]); // Second arg:  number of children

  // Server socket
  int servSock = SetupTCPServerSocket(service);

  // Fork limit-1 child processes
  for (int processCt = 0; processCt < processLimit - 1; processCt++) {
    // Fork child process and report any errors
    pid_t processID = fork();
    if (processID < 0)
      DieWithSystemMessage("fork() failed");
    else if (processID == 0) // If this is the child process
      ProcessMain(servSock);
  }

  // Execute last process in parent
  ProcessMain(servSock);
  // NOT REACHED
}

void ProcessMain(int servSock) {
  for (;;) { // Run forever
    int clntSock = AcceptTCPConnection(servSock);
    printf("with child process: %d\n", getpid());
    HandleTCPClient(clntSock);
  }
}

#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/wait.h>
#include "Practical.h"

int main(int argc, char *argv[]) {

  if (argc != 2) // Test for correct number of arguments
    DieWithUserMessage("Parameter(s)", "<Server Port/Service>");

  char *service = argv[1]; // First arg:  local port/service
  int servSock = SetupTCPServerSocket(service);
  if (servSock < 0)
    DieWithUserMessage("SetupTCPServerSocket() failed", "unable to establish");

  unsigned int childProcCount = 0; // Number of child processes
  for (;;) { // Run forever
    // New connection creates a client socket
    int clntSock = AcceptTCPConnection(servSock);
    // Fork child process and report any errors
    pid_t processID = fork();
    if (processID < 0)
      DieWithSystemMessage("fork() failed");
    else if (processID == 0) { // If this is the child process
      close(servSock);         // Child closes parent socket
      HandleTCPClient(clntSock);
      exit(0);                 // Child process terminates
    }

    printf("with child process: %d\n", processID);
    close(clntSock);  // Parent closes child socket descriptor
    childProcCount++; // Increment number of child processes

    while (childProcCount) { // Clean up all zombies
      processID = waitpid((pid_t) - 1, NULL, WNOHANG); // Non-blocking wait
      if (processID < 0) // waitpid() error?
        DieWithSystemMessage("waitpid() failed");
      else if (processID == 0) // No zombie to wait on
        break;
      else
        childProcCount--; // Cleaned up after a child
    }
  }
  // NOT REACHED
}

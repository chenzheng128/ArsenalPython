#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>
#include "Practical.h"

void InterruptSignalHandler(int signalType); // Interrupt signal handling function

int main(int argc, char *argv[]) {
  struct sigaction handler; // Signal handler specification structure

  // Set InterruptSignalHandler() as handler function
  handler.sa_handler = InterruptSignalHandler;
  // Create mask that blocks all signals
  if (sigfillset(&handler.sa_mask) < 0)
    DieWithSystemMessage("sigfillset() failed");
  handler.sa_flags = 0;  // No flags

  // Set signal handling for interrupt signal
  if (sigaction(SIGINT, &handler, 0) < 0)
    DieWithSystemMessage("sigaction() failed for SIGINT");

  for (;;)
    pause(); // Suspend program until signal received

  exit(0);
}

void InterruptSignalHandler(int signalType) {
  puts("Interrupt Received.  Exiting program.");
  exit(1);
}

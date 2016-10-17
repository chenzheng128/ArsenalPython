#include <iostream>
#include "PracticalSocket.h"
#include "SurveyCommon.h"

using namespace std;

int main(int argc, char *argv[]) {
  try {
    // Connect to the server's administrative interface.
    TCPSocket sock("localhost", SURVEY_PORT + 1);

    // Read the server's report a block at a time.
    char buffer[ 1025 ];
    int len;
    while ((len = sock.recv(buffer, sizeof(buffer) - 1)) != 0) {
      buffer[len] = '\0';               // Null terminate the sequence
      cout << buffer;                   // And print it like as a string
    }
  } catch(SocketException &e) {
    cerr << e.what() << endl;           // Report errors to the console.
    exit(1);
  }

  return 0;
}

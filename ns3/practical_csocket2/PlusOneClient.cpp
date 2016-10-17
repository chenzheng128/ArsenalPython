#include <iostream>
#include <cstdlib>
#include "PracticalSocket.h"

using namespace std;

int main(int argc, char *argv[]) {
  if (argc != 3) {                      // Check number of parameters
    cerr << "Usage: PlusOneClient <server host> <starting value>" << endl;
    return 1;
  }

  try {
    TCPSocket sock(argv[1], 9431);      // Connect to the server.

    uint32_t val = atoi(argv[2]);       // Parse user-suppled value
    val = ntohl(val);                   // Convert to network byte order
    sock.send(&val, sizeof(val));       // Send to server.

    // Read the server's response, convert to local byte order and print it
    if (sock.recvFully(&val, sizeof(val)) == sizeof(val)) {
      val = ntohl(val);
      cout << "Server Response: " << val << endl;
    }
    // Socket is closed when it goes out of scope
  } catch(SocketException &e) {
    cerr << e.what() << endl;
  }

  return 0;
}

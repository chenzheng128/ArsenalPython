#include <iostream>
#include <iomanip>
#include "PracticalSocket.h"
#include "SurveyCommon.h"

using namespace std;

int main(int argc, char *argv[]) {
  if (argc != 2) {                      // Make sure the user gives a host
    cerr << "Usage: SurveyClient <Survey Server Host>" << endl;
    return 1;
  }

  try {
    // Connect to the server.
    TCPSocket sock(argv[1], SURVEY_PORT);

    // Find out how many questions there are.
    int qCount = recvInt(&sock);
    for (int q = 0; q < qCount; q++) {
      // Show each the question to the user and print the list of responses.
      cout << "Q" << q << ":  " << recvString(&sock) << endl;
      int rCount = recvInt(&sock);
      for (int r = 0; r < rCount; r++)
        cout << setw(2) << r << " "  << recvString(&sock) << endl;

      // Keep prompting the user until we get a legal response.
      int response = rCount;
      while (response < 0 || response >= rCount) {
        cout << "> ";
        cin >> response;
      }

      // Send the server the user's response
      sendInt(&sock, response);
    }
  } catch(runtime_error &e) {
    cerr << e.what() << endl;           // Report errors to the console.
    return 1;
  }

  return 0;
}

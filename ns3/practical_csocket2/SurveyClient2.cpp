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
    iostream &stream = sock.getStream();
    vector<Question> qList;            // Read the whole survey
    readSurvey(stream, qList);

    for (unsigned int q = 0; q < qList.size(); q++) {
      // Show each the question to the user and print the list of responses.
      cout << "Q" << q << ":  " << qList[q].qText << endl;
      for (unsigned int r = 0; r < qList[q].rList.size(); r++)
        cout << setw(2) << r << " "  << qList[q].rList[r] << endl;

      // Keep prompting the user until we get a legal response.
      unsigned int response = qList[q].rList.size();
      while (response < 0 || response >= qList[q].rList.size()) {
        cout << "> ";
        cin >> response;
      }

      stream << response << endl;       // Send user response to server
      stream.flush();
    }
  } catch(SocketException &e) {
    cerr << e.what() << endl;           // Report errors to the console.
    return 1;
  }

  return 0;
}

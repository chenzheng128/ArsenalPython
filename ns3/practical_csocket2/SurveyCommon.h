#ifndef __SURVEYCOMMON_H__
#define __SURVEYCOMMON_H__

#include "PracticalSocket.h"
#include <string>
#include <vector>

/** Port number used by the Survey Server */
const in_port_t SURVEY_PORT = 12543;

/** Write an encoding of val to the socket, sock. */
void sendInt(CommunicatingSocket *sock, uint32_t val) throw(SocketException);

/** Write an encoding of str to the socket, sock. */
void sendString(CommunicatingSocket *sock, const std::string &str)
  throw(SocketException);

/** Read from sock a integer encoded by sendInt() and return it */
uint32_t recvInt(CommunicatingSocket *sock) throw(std::runtime_error);

/** Read from sock a string encoded by sendString() and return it */
std::string recvString(CommunicatingSocket *sock) throw(std::runtime_error);

/** Representation for a survey question */
struct Question {
  std::string qText;                    // Text of the question.
  std::vector<std::string> rList;       // List of response choices.
};

/** Read survey questions from the given stream and store them in qList. */
bool readSurvey(std::istream &stream, std::vector<Question> &qList);

#endif

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include "Practical.h"

static const char DELIMITER = '\n';

/* Read up to bufSize bytes or until delimiter, copying into the given
 * buffer as we go.
 * Encountering EOF after some data but before delimiter results in failure.
 * (That is: EOF is not a valid delimiter.)
 * Returns the number of bytes placed in buf (delimiter NOT transferred).
 * If buffer fills without encountering delimiter, negative count is returned.
 * If stream ends before first byte, -1 is returned.
 * Precondition: buf has room for at least bufSize bytes.
 */
int GetNextMsg(FILE *in, uint8_t *buf, size_t bufSize) {
  int count = 0;
  int nextChar;
  while (count < bufSize) {
    nextChar = getc(in);
    if (nextChar == EOF) {
      if (count > 0)
        DieWithUserMessage("GetNextMsg()", "Stream ended prematurely");
      else
        return -1;
    }
    if (nextChar == DELIMITER)
      break;
    buf[count++] = nextChar;
  }
  if (nextChar != DELIMITER) { // Out of space: count==bufSize
    return -count;
  } else { // Found delimiter
    return count;
  }
}

/* Write the given message to the output stream, followed by
 * the delimiter.  Return number of bytes written, or -1 on failure.
 */
int PutMsg(uint8_t buf[], size_t msgSize, FILE *out) {
  // Check for delimiter in message
  int i;
  for (i = 0; i < msgSize; i++)
    if (buf[i] == DELIMITER)
      return -1;
  if (fwrite(buf, 1, msgSize, out) != msgSize)
    return -1;
  fputc(DELIMITER, out);
  fflush(out);
  return msgSize;
}

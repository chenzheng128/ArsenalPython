/*
 *   C++ sockets on Unix and Windows
 *   Copyright (C) 2002
 *
 *   This program is free software; you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation; either version 2 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program; if not, write to the Free Software
 *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#ifndef __PRACTICALSOCKET_INCLUDED__
#define __PRACTICALSOCKET_INCLUDED__

#ifdef WIN32
#include <winsock2.h>        // For socket(), connect(), send(), and recv()
#include <ws2tcpip.h>

typedef int socklen_t;
typedef char raw_type;       // Type used for raw data on this platform

// Types to simplify portability, may not be necessary in the future.
typedef unsigned int uint32_t;
typedef unsigned short in_port_t;
#else
#include <sys/types.h>       // For data types
#include <sys/socket.h>      // For socket(), connect(), send(), and recv()
#include <netdb.h>           // For gethostbyname(), in_port_t
#include <arpa/inet.h>       // For inet_addr()
#include <unistd.h>          // For close()
#include <netinet/in.h>      // For sockaddr_in
typedef void raw_type;       // Type used for raw data on this platform
#endif

#include <iostream>
#include <string>
#include <stdexcept>
#include <vector>

/**
 *   Signals a problem with the execution of a socket call.
 */
class SocketException : public std::runtime_error {
public:
  /**
   *   Construct a SocketException with a user message followed by a
   *   system detail message.
   *   @param message explanatory message
   */
  SocketException(const std::string &message) throw();
  
  /**
   *   Construct a SocketException with a explanatory message.
   *   @param message explanatory message
   *   @param detail detail message
   */
  SocketException(const std::string &message, const std::string &detail) throw();
};

/** 
    Container aggregating an address and a port for a socket.
    SocketAddress offers value semantics.
*/
class SocketAddress {
public:
  /** Type of address being requested. */
  enum AddressType { TCP_SOCKET, TCP_SERVER, UDP_SOCKET };
  
  /** Make a SocketAddress for the given host and service. */
  SocketAddress(const char *host, const char *service,
                AddressType atype = TCP_SOCKET) throw(SocketException);

  /** Make a SocketAddress for the given host and port number. */
  SocketAddress(const char *host, in_port_t port,
                AddressType atype = TCP_SOCKET) throw(SocketException);

  /** Make a SocketAddress that wraps a copy of the given sockaddr
      structure of the given addreLenVal legth in bytes.  If used as a
      default constructur, the SocketAddress is created in an
      uninitialized state, and none of its get methods should be used
      until it is initialized. */
  SocketAddress(sockaddr *addrVal = NULL, socklen_t addrLenVal = 0);

  /** Return a string representation of the address portion of this
      object. */
  std::string getAddress() const throw(SocketException);

  /** Return a numeric value for the port portion of this object. */
  in_port_t getPort() const throw(SocketException);

  /** Return a pointer to the sockaddr structure wrapped by this object. */
  sockaddr *getSockaddr() const {
    return (sockaddr *)&addr;
  }

  /** Return the length of the sockaddr structure wrapped by this object. */
  socklen_t getSockaddrLen() const {
    return addrLen;
  }

  /** Return a list of all matching addresses for the given host and
      service.  Either, but not both of host and service can be null.
      The returned list of addresses may be empty. */
  static std::vector<SocketAddress> 
    lookupAddresses(const char *host, const char *service,
                    AddressType atype = TCP_SOCKET) throw(SocketException);

  /** Return a list of all matching addresses for the given host and
      port.  Either, but not both of host and service can be null (or
      zero).  The returned list of addresses may be empty. */
  static std::vector<SocketAddress> 
    lookupAddresses(const char *host, in_port_t port,
                    AddressType atype = TCP_SOCKET) throw(SocketException);

private:
  // Raw address portion of this object.
  sockaddr_storage addr;

  // Number of bytes used in the addr field.
  socklen_t addrLen;
};

class Socket {
public:
  virtual ~Socket();

  /**
   *   Get the local address
   *   @return local address of socket
   *   @exception SocketException thrown if fetch fails
   */
  SocketAddress getLocalAddress() throw(SocketException);

  /** Close this socket. */
  void close();

  /**
   *   If WinSock, unload the WinSock DLLs; otherwise do nothing.  We ignore
   *   this in our sample client code but include it in the library for
   *   completeness.  If you are running on Windows and you are concerned
   *   about DLL resource consumption, call this after you are done with all
   *   Socket instances.  If you execute this on Windows while some instance of
   *   Socket exists, you are toast.  For portability of client code, this is 
   *   an empty function on non-Windows platforms so you can always include it.
   *   @param buffer buffer to receive the data
   *   @param bufferLen maximum number of bytes to read into buffer
   *   @return number of bytes read, 0 for EOF, and -1 for error
   *   @exception SocketException thrown WinSock clean up fails
   */
  static void cleanUp() throw(SocketException);

private:
  // Prevent the user from trying to use value semantics on this object
  Socket(const Socket &sock);
  void operator=(const Socket &sock);

protected:
  /** Socket descriptor, protected so derived classes can read it
      easily (may want to change this) */
  int sockDesc;

  /** You can only construct this object via a derived class. */
  Socket();

  void createSocket(const SocketAddress &address, int type,
                    int protocol) throw(SocketException);
};

/**
 *   Abstract base class representing a socket that, once connected, has
 *   a foreign address and can communicate with the socket at that foreign
 *   address.
 */
class CommunicatingSocket : public Socket {
public:
  /**
   *   Write bufferLen bytes from the given buffer to this socket.
   *   The socket must be connected before send() can be called.
   *   @param buffer buffer to be written
   *   @param bufferLen number of bytes from buffer to be written
   *   @exception SocketException thrown if unable to send data
   */
  void send(const void *buffer, int bufferLen) throw(SocketException);

  /**
   *   Read into the given buffer up to bufferLen bytes data from this
   *   socket.  The socket must be connected before recv can be called.
   *   @param buffer buffer to receive the data
   *   @param bufferLen maximum number of bytes to read into buffer
   *   @return number of bytes read, 0 for EOF.
   *   @exception SocketException thrown if unable to receive data
   */
  size_t recv(void *buffer, int bufferLen) throw(SocketException);

  /**
   *   Block until bufferLen bytes are read into the given buffer,
   *   until the socket is closed or an error is encoutered.  The
   *   socket must be connected before recvFully can be called.
   *   @param buffer buffer to receive the data
   *   @param bufferLen maximum number of bytes to read into buffer
   *   @return number of bytes read, 0 for EOF, and -1 for error
   *   @exception SocketException thrown if unable to receive data
   */
  size_t recvFully(void *buffer, int bufferLen) throw(SocketException);

  /**
   *   Get the address of the peer to which this socket is connected.
   *   The socket must be connected before this method can be called.
   *   @return foreign address
   *   @exception SocketException thrown if unable to fetch foreign address
   */
  SocketAddress getForeignAddress() throw(SocketException);
};

/**
 *   TCP socket for communication with other TCP sockets
 */
class TCPSocket : public CommunicatingSocket {
public:
  /**
     Make a socket that is neither bound nor connected.
   */
  TCPSocket();

  ~TCPSocket();

  /**
   *   Construct a TCP socket with a connection to the given foreign
   *   address and port.  This is interface is provided as a convience
   *   for typical applications that don't need to worry about the
   *   local address and port.  
   *   @param foreignAddress foreign address (IP address or name) 
   *   @param foreignPort foreign port 
   *   @exception SocketException thrown if unable to create TCP socket
   */
  TCPSocket(const char *foreignAddress, in_port_t foreignPort) 
    throw(SocketException);

  /**
     Bind this socket to the given local address.
   */
  void bind(const SocketAddress &localAddress) throw(SocketException);
  
  /**
     Connect this socket to the given foreign address.
   */
  void connect(const SocketAddress &foreignAddress) throw(SocketException);

  /**
   *   Return a reference to an I/O stream wrapper around this
   *   CommunicatingSocket.  The caller can use this object to send
   *   and receive text-encoded messages over the socket.  The returned
   *   stream is owned by the socket and is created on the first call
   *   to getStream.
   */
  std::iostream &getStream() throw(SocketException);

private:
  // Access for TCPServerSocket::accept() connection creation
  friend class TCPServerSocket;
  TCPSocket(int sockDesc);

  /** iostream associated with this socket, or NULL if it doesn't have
      one. */
  std::iostream *myStream;

  /** Streambuffer managed by myStream. */
  std::streambuf *myStreambuf;
};

/**
 *   TCP socket class for servers
 */
class TCPServerSocket : public Socket {
public:
  /**
     Make an unbound socket.
   */
  TCPServerSocket();

  /**
   *   Construct a TCP socket for use with a server, accepting connections
   *   on the specified port on any interface
   *   @param localPort local port of server socket, a value of zero will
   *                   give a system-assigned unused port
   *   @param queueLen maximum queue length for outstanding 
   *                   connection requests (default 5)
   *   @exception SocketException thrown if unable to create TCP server socket
   */
  TCPServerSocket(in_port_t localPort, int queueLen = 5) 
      throw(SocketException);

  /**
     Bind this socket to the given local address.
   */
  void bind(const SocketAddress &localAddress) throw(SocketException);
  
  /**
   *   Blocks until a new connection is established on this socket or error
   *   @return new connection socket
   *   @exception SocketException thrown if attempt to accept a new connection fails
   */
  TCPSocket *accept() throw(SocketException);

private:
  void setListen(int queueLen) throw(SocketException);
};

/**
  *   UDP socket class
  */
class UDPSocket : public Socket {
public:
  /**
   *   Construct a UDP socket
   *   @exception SocketException thrown if unable to create UDP socket
   */
  UDPSocket();

  void bind(const SocketAddress &localAddress) throw(SocketException);

  void connect(const SocketAddress &foreignAddress) throw(SocketException);

  /**
   *   Unset foreign address and port
   *   @return true if disassociation is successful
   *   @exception SocketException thrown if unable to disconnect UDP socket
   */
  void disconnect() throw(SocketException);

  /**
   *   Send the given buffer as a UDP datagram to the
   *   specified address/port
   *   @param buffer buffer to be written
   *   @param bufferLen number of bytes to write
   *   @param foreignAddress address to send to
   *   @exception SocketException thrown if unable to send datagram
   */
  void sendTo(const void *buffer, int bufferLen,
              const SocketAddress &foreignAddress) throw(SocketException);

  /**
   *   Read read up to bufferLen bytes data from this socket.  The given buffer
   *   is where the data will be placed
   *   @param buffer buffer to receive data
   *   @param bufferLen maximum number of bytes to receive
   *   @param sourceAddress address of datagram source
   *   @param sourcePort port of data source
   *   @return number of bytes received and -1 for error
   *   @exception SocketException thrown if unable to receive datagram
   */
  int recvFrom(void *buffer, int bufferLen, 
               SocketAddress &sourceAddress) throw(SocketException);

  /**
   *   Set the multicast TTL
   *   @param multicastTTL multicast TTL
   *   @exception SocketException thrown if unable to set TTL
   */
  void setMulticastTTL(unsigned char multicastTTL) throw(SocketException);

  /**
   *   Join the specified multicast group
   *   @param multicastGroup multicast group address to join
   *   @exception SocketException thrown if unable to join group
   */
  void joinGroup(const std::string &multicastGroup) throw(SocketException);

  /**
   *   Leave the specified multicast group
   *   @param multicastGroup multicast group address to leave
   *   @exception SocketException thrown if unable to leave group
   */
  void leaveGroup(const std::string &multicastGroup) throw(SocketException);

private:
  void setBroadcast();
};

#endif

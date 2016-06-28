
#CFLAGS = -g -Wall -O3
CFLAGS = -g -O3 -w # disable warning

BIN1=ex37.client
BIN2=ex37.server


all: udp-send udp-recv $(BIN1) $(BIN2)

## adabook code ##
$(BIN1): $(BIN1).o wrap.o
	$(CC) wrap.o $(BIN1).o -o $(BIN1)

$(BIN2): $(BIN2).o wrap.o
    # TODO adabook 代码 $(BIN2) Server不能正常工作(一接受数据就崩溃), 待改进
	$(CC) wrap.o $(BIN2).o -o $(BIN2)

wrap.o:

$(BIN1).o: $(BIN1).c wrap.h

$(BIN2).o: $(BIN2).c wrap.h

## cs417 code ##
udp-send: udp-send.o
	$(CC) -o udp-send udp-send.o $(LIBS)

udp-recv: udp-recv.o
	$(CC) -o udp-recv udp-recv.o $(LIBS)

udp-send.o: udp-send.c port.h

udp-recv.o: udp-recv.c port.h


clean:
	rm -f $(BIN1)
	rm -f $(BIN2)
	rm -f *.o
	rm -f udp-send udp-recv udp-send.o udp-recv.o


run:
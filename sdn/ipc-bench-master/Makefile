
#CFLAGS = -g -Wall -O3
CFLAGS = -g -O3 -w # disable warning

build: \
	tc_shell_lat \
	tc_shell_p_lat \
	udp_lat \
	tcp_lat \
	unix_lat_client \
	unix_lat_server \
	unix_lat


all: pipe_lat pipe_thr \
	unix_lat unix_thr \
	tcp_lat tcp_thr \
	get_tc_queue_lat \
	tc_shell_lat \
	tcp_local_lat tcp_remote_lat


run:
	./pipe_lat 100 10000
	./unix_lat 100 10000
	./tcp_lat 100 10000
	./pipe_thr 100 10000
	./unix_thr 100 10000
	./tcp_thr 100 10000

clean:
	#rm -f *.o
	rm -f *~ core
	rm -f pipe_lat pipe_thr
	rm -f unix_lat unix_thr
	rm -f tcp_lat tcp_thr
	rm -f tcp_local_lat tcp_remote_lat
	rm -f tc_shell_p_lat
	rm -f tc_shell_lat
	rm -f udp_lat
	rm -f unix_lat_server unix_lat_client

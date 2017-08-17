# 默认参数运行Fig
DEFAULT_OUT=output/4.0-2-100-25-0.0-dctcp
DEFAULT_ENVS=tmin=4.0 flownum=2 tcpstartinterval=0.0

install_deps:
	sudo apt-get update
	#  去掉 mono-devel 感觉没什么用; mono 是 Cross platform, open source .NET framework
	sudo apt-get -y install vlan libssl-dev libncurses5-dev python-matplotlib python-numpy
	sudo apt-get -y install build-essential autoconf automake libxmu-dev xorg-dev g++ xgraph
	# cd ns-2 && tar -xvf ns-allinone-2.34.tar.gz
	# cd ns-2/ns-allinone-2.34/ && patch -p1 < ../qjump-ns2/ns-allinone-2.34.ubuntu.patch
	# cd ns-2/ns-allinone-2.34/ && ./install
	# cd ns-2/ns-allinone-2.34/ns-2.34/ && patch -p1 < ../../qjump-ns2/pfabric.patch && make clean && make
	./bin/make_settings.py

settings:
	./bin/make_settings.py

clean:
	rm ${TCL_DIR}/out/*

run:
	mkdir -p $DEFAULT_OUT
	cd $(DEFAULT_OUT); \
		$(DEFAULT_ENVS) \
		python ../../run_sim.py --fig_1 --fig_13 --fig_14
	
	# echo "Please navigate to:  http://<IP_ADDRESS>:8002 in your browser to view the results."
	# sudo python -m SimpleHTTPServer 8002

run1:
	mkdir -p $(DEFAULT_OUT)
	cd $(DEFAULT_OUT); \
		$(DEFAULT_ENVS) \
		python ../../run_sim.py --fig_1
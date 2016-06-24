#!/usr/bin/python
#--*-- coding:utf-8 --*--

from mininet.log import lg, LEVELS, info, debug, warn, error
import os, sys, re
import time

# """
# 遍历统计端口的 tc 状态
# author: zhchen@cuc.edu.cn
# REF: HTB Linux queuing discipline manual - user guide
#   http://luxik.cdi.cz/~devik/qos/htb/manual/userg.htm
# """

#HOST_PORT="h1-"
#host_ports=["h1-eth0", "h2-eth0", ]
SW_PORTS="s1-eth1 s1-eth2 s1-eth3 s3-eth1 s3-eth2 s4-eth1 s4-eth2 s2-eth1 s2-eth2 s2-eth3"
sw_ports=SW_PORTS.split()

def show_qdisc():
    #print SW_PORTS
    #print sw_ports
    print "查看设备 qdisc: tc qdisc show dev <PORT>"
    for port in sw_ports:
        result = [port] + os.popen('tc qdisc show dev %s' % (port)).readlines()
        print result

def show_class():
    #print SW_PORTS
    #print sw_ports
    print "查看设备 class:  tc class show dev <PORT>"
    for port in sw_ports:
        result = [port] + os.popen('tc class show dev %s' % (port)).readlines()
        print result

def show_qdisc_errors_once(show_all=True):
    """
    :param show_all:
    :return:
    show_all=True  默认打印所有网卡的数据
    show_all=False 仅显示在 watch_attrs 中存在异常的网卡数据.
     数据获取方法: tc -s -d qdisc show dev s1-eth3
     如发现丢包, 在设置 class 的网卡上, 可以通过 show_class_watch_values() 进行详细监视查看
      tc -s -d class show dev s1-eth3

    """

    extract_attrs="pfifo_fast netem htb rate" # Sent Bytes " #总是打印的数据属性
    watch_attrs=" dropped overlimits requeues " #不仅打印而且关心非0的数据
    suffix_attrs=" Sent Bytes " #追加数据
    all_data_attrs= extract_attrs+watch_attrs+suffix_attrs

    #print SW_PORTS
    #print sw_ports
    print "查看设备 drops:  tc -s -d qdisc show dev <PORT>"
    for port in sw_ports:
        #[port]
        result = os.popen('tc -s -d qdisc show dev %s ' % (port)).readlines()
        result = " ".join(result).replace("\n", " ").strip().split("class ")
        for line in result:
            #x = re.findall('^From .* ([0-9][0-9]):', line)
            qclass = port + " "
            watched=False #是否发现我们想要的值
            for attr_name in (all_data_attrs).split():
                # dropped[\(\s]([^\s\)\,]+)[ \)\s,] 在这里很好测试re https://regex101.com/#python
                attr_value = re.findall(attr_name+"[\(\s]([^\s\)\,]+)[ \)\s,]", line) #search dropped 0
                if len(attr_value)>0:
                    qclass += " " + attr_name + " " + attr_value[0]
                    #print attr_name + " " + attr_value[0]
                    #print qclass
                    if watch_attrs.find(attr_name)!=-1 and attr_value[0]!='0':
                        watched=True #找到了非0数据,设置 打印标志

            if show_all or watched : print qclass #打印
        #break

def show_class_watch_values(attr_name):
    """
    没有任何filter策略时候的拥塞位置
     tc -s -d class show dev s1-eth3
    :return:
    """
    #print SW_PORTS
    #print sw_ports
    print "查看设备class drops:  tc -s -d class show dev <PORT>"
    header_print = False
    while True:
        time.sleep(1)
        if header_print == False: #打印表头\\
            header_str = attr_name + " "
            for port in sw_ports:
                #[port]
                #if (port.startswith("s1")) or (port.startswith("s2")):
                    #print port
                    header_str += port + " "
                    result = os.popen('tc class show dev %s ' % (port)).readlines()

                    qclasses = " ".join(result).replace("\n", " ").strip().split("class ")

                    for line in qclasses:
                        attr_value = re.findall("htb[\(\s]([^\s\)\,]+)[ \)\s,]", line) #search dropped 0
                        if len(attr_value)>0:
                            header_str += attr_value[0]+" "
            print header_str
            header_print = True


        row_str=attr_name + " "
        for port in sw_ports:
            #if (port.startswith("s1")) or (port.startswith("s2")):
                row_str += port + " "
                result = os.popen('tc -s -d class show dev %s ' % (port)).readlines()
                qclasses = " ".join(result).replace("\n", " ").strip().split("class ")
                for line in qclasses:
                    attr_value = re.findall(attr_name+"[\(\s]([^\s\)\,]+)[ \)\s,]", line) #search dropped 0
                    if len(attr_value)>0:
                         row_str += attr_value[0]+" "
        print row_str


def show_watch_dropped():
    print "显示 tc dropped 丢包情况"
    DROPPED="dropped"
    show_class_watch_values(DROPPED)

def runner():
    #show_qdisc()
    #show_class()
    #show_qdisc_errors_once()
    show_watch_dropped()


if __name__ == "__main__":
    try:
        runner()
    except KeyboardInterrupt:
        info( "\n\nKeyboard Interrupt. Shutting down and cleaning up...\n\n")
        #cleanup()
    except Exception:
        # Print exception
        type_, val_, trace_ = sys.exc_info()
        errorMsg = ( "-"*80 + "\n" +
                     "Caught exception. Cleaning up...\n\n" +
                     "%s: %s\n" % ( type_.__name__, val_ ) +
                     "-"*80 + "\n" )
        error( errorMsg )
        # Print stack trace to debug log
        import traceback
        stackTrace = traceback.format_exc()
        debug( stackTrace + "\n" )
        #cleanup()

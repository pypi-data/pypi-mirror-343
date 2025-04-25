from pickle import TRUE
import time
#from scapy.all import *
import collections
from binascii import hexlify
import logging
from enum import Enum
from pprint import pprint
import hashlib
import ipaddress
import random
import os
import ipaddress
import bisect
import sys
from collections import deque 
import random
import socket
import psutil
import requests
import datetime
import sys
from sys import platform
import platform as platforminfo
import datetime
import multiprocessing
from collections import OrderedDict
#from scapy.all import *
import queue
import string

import time
import queue
import sys
import requests

import collections


import dpkt
import socket
from collections import defaultdict







import warnings
warnings.filterwarnings("ignore")

#import packet_info


import datetime
import threading
import os

import argparse
import configparser
import json

'''#Not needed, just to avoid code analysis errors
from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import ARP
from scapy.layers.l2 import Ether'''

import cProfile
import re


benchmark_times=[]

verbose=1
if verbose == 0:
    logging.root.setLevel(logging.NOTSET)
    logging.basicConfig(level=logging.NOTSET)
elif verbose == 1:
    logging.root.setLevel(logging.WARNING)
    logging.basicConfig(level=logging.WARNING)
elif verbose == 2:
    logging.root.setLevel(logging.ERROR)
    logging.basicConfig(level=logging.ERROR)



COMMON_PORTS = {
    1201,1213,1216,1217,1218,1233,1234,1236,1244,
    1247,1248,1259,1271,1272,1277,1287,1296,1300,1301,1309,1310,1311,1322,1328,1334,
    1352,1417,1433,1434,1443,1455,1461,1494,1500,1501,1503,1521,1524,1533,1556,1580,
    1583,1594,1600,1641,1658,1666,1687,1688,1700,1717,1718,1719,1720,1721,1723,1755,
    1761,1782,1783,1801,1805,1812,1839,1840,1862,1863,1864,1875,1900,1914,1935,1947,
    1971,1972,1974,1984,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,
    2010,2013,2020,2021,2022,2030,2033,2034,2035,2038,2040,2041,2042,2043,2045,2046,
    2047,2048,2049,2065,2068,2099,2100,2103,2105,2106,2107,2111,2119,2121,2126,2135,
    2144,2160,2161,2170,2179,2190,2191,2196,2200,2222,2251,2260,2288,2301,2323,2366,
    2381,2382,2383,2393,2394,2399,2401,2492,2500,2522,2525,2557,2601,2602,2604,2605,
    2607,2608,2638,2701,2702,2710,2717,2718,2725,2800,2809,2811,2869,2875,2909,2910,
    2920,2967,2968,2998,3000,3001,3003,3005,3006,3007,3011,3013,3017,3030,3031,3052,
    3071,3077,3128,3168,3211,3221,3260,3261,3268,3269,3283,3300,3301,3306,3322,3323,
    3324,3325,3333,3351,3367,3369,3370,3371,3372,3389,3390,3404,3476,3493,3517,3527,
    3546,3551,3580,3659,3689,3690,3703,3737,3766,3784,3800,3801,3809,3814,3826,3827,
    3828,3851,3869,3871,3878,3880,3889,3905,3914,3918,3920,3945,3971,3986,3995,3998,
    4000,4001,4002,4003,4004,4005,4006,4045,4111,4125,4126,4129,4224,4242,4279,4321,
    4343,4443,4444,4445,4446,4449,4550,4567,4662,4848,4899,4900,4998,5000,5001,5002,
    5003,5004,5009,5030,5033,5050,5051,5054,5060,5061,5080,5087,5100,5101,5102,5120,
    5190,5200,5214,5221,5222,5225,5226,5269,5280,5298,5357,5405,5414,5431,5432,5440,
    5500,5510,5544,5550,5555,5560,5566,5631,5633,5666,5678,5679,5718,5730,5800,5801,
    5802,5810,5811,5815,5822,5825,5850,5859,5862,5877,5900,5901,5902,5903,5904,5906,
    5907,5910,5911,5915,5922,5925,5950,5952,5959,5960,5961,5962,5963,5987,5988,5989,
    5998,5999,6000,6001,6002,6003,6004,6005,6006,6007,6009,6025,6059,6100,6101,6106,
    6112,6123,6129,6156,6346,6389,6502,6510,6543,6547,6565,6566,6567,6580,6646,6666,
    6667,6668,6669,6689,6692,6699,6779,6788,6789,6792,6839,6881,6901,6969,7000,7001,
    7002,7004,7007,7019,7025,7070,7100,7103,7106,7200,7201,7402,7435,7443,7496,7512,
    7625,7627,7676,7741,7777,7778,7800,7911,7920,7921,7937,7938,7999,8000,8001,8002,
    8007,8008,8009,8010,8011,8021,8022,8031,8042,8045,8080,8081,8082,8083,8084,8085,
    8086,8087,8088,8089,8090,8093,8099,8100,8180,8181,8192,8193,8194,8200,8222,8254,
    8290,8291,8292,8300,8333,8383,8400,8402,8443,8500,8600,8649,8651,8652,8654,8701,
    8800,8873,8888,8899,8994,9000,9001,9002,9003,9009,9010,9011,9040,9050,9071,9080,
    9081,9090,9091,9099,9100,9101,9102,9103,9110,9111,9200,9207,9220,9290,9415,9418,
    9485,9500,9502,9503,9535,9575,9593,9594,9595,9618,9666,9876,9877,9878,9898,9900,
    9917,9929,9943,9944,9968,9998,9999,10000,10001,10002,10003,10004,10009,10010,
    10012,10024,10025,10082,10180,10215,10243,10566,10616,10617,10621,10626,10628,
    10629,10778,11110,11111,11967,12000,12174,12265,12345,13456,13722,13782,13783,
    14000,14238,14441,14442,15000,15002,15003,15004,15660,15742,16000,16001,16012,
    16016,16018,16080,16113,16992,16993,17877,17988,18040,18101,18988,19101,19283,
    19315,19350,19780,19801,19842,20000,20005,20031,20221,20222,20828,21571,22939,
    23502,24444,24800,25734,25735,26214,27000,27352,27353,27355,27356,27715,28201,
    30000,30718,30951,31038,31337,32768,32769,32770,32771,32772,32773,32774,32775,
    32776,32777,32778,32779,32780,32781,32782,32783,32784,32785,33354,33899,34571,
    34572,34573,35500,38292,40193,40911,41511,42510,44176,44442,44443,44501,45100,
    48080,49152,49153,49154,49155,49156,49157,49158,49159,49160,49161,49163,49165,
    49167,49175,49176,49400,49999,50000,50001,50002,50003,50006,50300,50389,50500,
    50636,50800,51103,51493,52673,52822,52848,52869,54045,54328,55055,55056,55555,
    55600,56737,56738,57294,57797,58080,60020,60443,61532,61900,62078,63331,64623,
    64680,65000,65129,65389
}

# packet_info.py
import dpkt
import datetime
import socket
import struct
from collections import namedtuple


def parse_ethernet(packet_bytes, datalink):
    """
    Parse the packet bytes using the appropriate dpkt class based on the datalink type.
    """
    # DLT_EN10MB = 1: Standard Ethernet.
    if datalink == dpkt.pcap.DLT_EN10MB:
        try:
            eth = dpkt.ethernet.Ethernet(packet_bytes)
        except Exception as e:
            raise Exception(f"Ethernet parsing failed: {e}")
    # DLT_LINUX_SLL = 113: Linux cooked capture.
    elif datalink == 113:
        try:
            # dpkt.sll.SLL parses Linux cooked capture packets.
            # Note: SLL packets don't automatically convert to an Ethernet frame,
            # so we might need to adjust how we extract the IP packet.
            sll = dpkt.sll.SLL(packet_bytes)
            # sll.data should contain the encapsulated packet. In many cases it is already an IP packet.
            if not isinstance(sll.data, dpkt.ip.IP):
                raise Exception("Not an IP packet inside SLL")
            eth = sll  # We use the SLL object as our 'eth' equivalent.
        except Exception as e:
            raise Exception(f"Linux cooked capture parsing failed: {e}")
    else:
        raise Exception(f"Unsupported datalink type: {datalink}")
    return eth

#begin packetin
# Define the namedtuple for packet information.
PacketInfo = namedtuple("PacketInfo", [
    "packet_num", "proto", "packet_time",
    "ip_version", "ip_ihl", "ip_tos", "ip_len", "ip_id", "ip_flags", "ip_frag",
    "ip_ttl", "ip_proto", "ip_chksum", "ip_src", "ip_dst", "ip_options",
    "tcp_sport", "tcp_dport", "tcp_seq", "tcp_ack", "tcp_dataofs",
    "tcp_reserved", "tcp_flags", "tcp_window", "tcp_chksum", "tcp_urgptr", "tcp_options"
])


def ip_flags_to_str(flags_value):
    """Convert an integer flags value to a comma-separated string."""
    flag_names = []
    if flags_value & 0x2:
        flag_names.append("DF")
    if flags_value & 0x1:
        flag_names.append("MF")
    return ",".join(flag_names) if flag_names else ""


def tcp_flags_to_str(flags_value):
    """Convert dpkt TCP flags value to a comma-separated string."""
    flag_names = []
    if flags_value & dpkt.tcp.TH_FIN:
        flag_names.append("FIN")
    if flags_value & dpkt.tcp.TH_SYN:
        flag_names.append("SYN")
    if flags_value & dpkt.tcp.TH_RST:
        flag_names.append("RST")
    if flags_value & dpkt.tcp.TH_PUSH:
        flag_names.append("PSH")
    if flags_value & dpkt.tcp.TH_ACK:
        flag_names.append("ACK")
    if flags_value & dpkt.tcp.TH_URG:
        flag_names.append("URG")
    return ",".join(flag_names) if flag_names else ""

import struct, socket, datetime
import dpkt

ETH_HDR_LEN = 14          # without VLAN
ETH_P_IP    = 0x0800
ETH_P_8021Q = 0x8100      # VLANtagged frame

def parse_packet_info_fast(buf: bytes, pkt_no: int) -> PacketInfo:

    # --- L2 ----------------------------------------------------------------
    eth_type = struct.unpack('!H', buf[12:14])[0]
    off = ETH_HDR_LEN
    if eth_type == ETH_P_8021Q:          # 802.1Q VLAN tag adds 4bytes
        eth_type = struct.unpack('!H', buf[16:18])[0]
        off += 4
    if eth_type != ETH_P_IP:
        raise Exception("Not IPv4")

    # --- L3 (IP) -----------------------------------------------------------
    ip = dpkt.ip.IP(buf[off:])           # parses only the IPpacket
    if ip.p != dpkt.ip.IP_PROTO_TCP:
        raise Exception("Not TCP")

    ip_hdr_len = ip.hl * 4               # cached for TCP offset
    ip_flags   = ip_flags_to_str(ip.off >> 13)

    # --- L4 (TCP) ----------------------------------------------------------
    tcp_off = off + ip_hdr_len
    tcp = dpkt.tcp.TCP(buf[tcp_off:])    # direct slice, no reparse of L2/L3

    # --- populate ----------------------------------------------------------
    return PacketInfo(
        packet_num   = pkt_no,
        proto        = "TCP",
        packet_time  = datetime.datetime.now().timestamp(),

        ip_version   = ip.v,
        ip_ihl       = ip.hl,
        ip_tos       = ip.tos,
        ip_len       = ip.len,
        ip_id        = ip.id,
        ip_flags     = ip_flags,
        ip_frag      = ip.off & 0x1FFF,
        ip_ttl       = ip.ttl,
        ip_proto     = ip.p,
        ip_chksum    = ip.sum,
        ip_src       = socket.inet_ntoa(ip.src),
        ip_dst       = socket.inet_ntoa(ip.dst),
        ip_options   = ip.opts.hex() if ip.opts else "",

        tcp_sport    = tcp.sport,
        tcp_dport    = tcp.dport,
        tcp_seq      = tcp.seq,
        tcp_ack      = tcp.ack,
        tcp_dataofs  = tcp.off * 4,
        tcp_reserved = 0,
        tcp_flags    = tcp_flags_to_str(tcp.flags),
        tcp_window   = tcp.win,
        tcp_chksum   = tcp.sum,
        tcp_urgptr   = tcp.urp,
        tcp_options  = tcp.opts.hex() if tcp.opts else ""
    )


def parse_packet_info(packet_bytes, packet_number, datalink=dpkt.pcap.DLT_EN10MB):
    """
    Parse raw packet bytes using dpkt and return a PacketInfo namedtuple.
    
    Raises:
        Exception: if the packet is not Ethernet/IP/TCP.
    """
    # Use current timestamp (you could use a timestamp from a pcap if available)
    packet_time = datetime.datetime.now().timestamp()
    
    # Parse the Ethernet frame.
    try:
        eth = dpkt.ethernet.Ethernet(packet_bytes)
    except Exception as e:
        raise Exception(f"Could not parse Ethernet frame: {e}")
    
    # Depending on the datalink type, the IP packet may be in different attributes.
    # For Ethernet, the payload is in eth.data.
    if not isinstance(eth.data, dpkt.ip.IP):
        raise Exception("Not an IP packet")
    ip = eth.data

    # Ensure the IP payload is a TCP segment.
    if not isinstance(ip.data, dpkt.tcp.TCP):
        raise Exception("Not a TCP packet")
    tcp = ip.data

    # Extract IP header fields.
    ip_version = ip.v
    ip_ihl = ip.hl
    ip_tos = ip.tos
    ip_len = ip.len
    ip_id = ip.id
    # ip.off encodes the flags in the upper 3 bits and fragment offset in the lower 13 bits.
    ip_flags_value = ip.off >> 13
    ip_flags = ip_flags_to_str(ip_flags_value)
    ip_frag = ip.off & 0x1FFF
    ip_ttl = ip.ttl
    ip_proto = ip.p if hasattr(ip, 'p') else ip.proto
    ip_chksum = ip.sum if hasattr(ip, 'sum') else ip.chksum
    ip_src = socket.inet_ntoa(ip.src)
    ip_dst = socket.inet_ntoa(ip.dst)
    ip_options = ip.opts.hex() if hasattr(ip, 'opts') and ip.opts else ""

    # Extract TCP header fields.
    tcp_sport = tcp.sport
    tcp_dport = tcp.dport
    tcp_seq = tcp.seq
    tcp_ack = tcp.ack
    tcp_dataofs = tcp.off * 4  # dpkt.tcp.TCP.off is in 32-bit words.
    tcp_reserved = 0  # dpkt does not provide reserved bits directly.
    tcp_flags = tcp_flags_to_str(tcp.flags)
    tcp_window = tcp.win
    tcp_chksum = tcp.sum if hasattr(tcp, 'sum') else tcp.chksum
    tcp_urgptr = tcp.urp
    tcp_options = tcp.opts.hex() if hasattr(tcp, 'opts') and tcp.opts else ""

    # Return the PacketInfo named tuple.
    return PacketInfo(
        packet_num=packet_number,
        proto="TCP",
        packet_time=packet_time,
        ip_version=ip_version,
        ip_ihl=ip_ihl,
        ip_tos=ip_tos,
        ip_len=ip_len,
        ip_id=ip_id,
        ip_flags=ip_flags,
        ip_frag=ip_frag,
        ip_ttl=ip_ttl,
        ip_proto=ip_proto,
        ip_chksum=ip_chksum,
        ip_src=ip_src,
        ip_dst=ip_dst,
        ip_options=ip_options,
        tcp_sport=tcp_sport,
        tcp_dport=tcp_dport,
        tcp_seq=tcp_seq,
        tcp_ack=tcp_ack,
        tcp_dataofs=tcp_dataofs,
        tcp_reserved=tcp_reserved,
        tcp_flags=tcp_flags,
        tcp_window=tcp_window,
        tcp_chksum=tcp_chksum,
        tcp_urgptr=tcp_urgptr,
        tcp_options=tcp_options
    )




def print_packet_info(pkt):
    for field, value in pkt._asdict().items():
        print(f"print_packet_info: {field}: {value}")

        
class Ports:
    def __init__(self,report_output_buffer,internalip,externalip,verbose,database,internal_is_private,external_is_private,internal_ip_equals_external_ip,interface,external_network_information,internal_network_information):
        print(f"Monitoring {internalip}")

        self.report_output_buffer=report_output_buffer
        self.unprocessed_packed_buffer=[]
        self.currently_open_ip_list = {}
        self.previously_open_ip_list_A = {}
        self.previously_open_ip_list_B = {}
        self.previously_open_ip_list_ptr=self.previously_open_ip_list_A
        self.previously_open_ip_list_ptr["time_started"]=0
        self.report_unwanted=[]

        self.packets_to_watch = OrderedDict()      # key -> list[Packet]



        self.ARP_requests = collections.deque()
        self.ARP_same_timestamp = collections.deque()
        self.timer=0
        self.SYN_reply_timeout=3
        self.ARP_reply_timeout=0.5
        self.Recently_closed_port_timeout=600
        
        
        self.num_total_tcp_packets=0
        self.num_unwanted_tcp_packets=0
        

        self.check_if_ip_changed_packet_interval=2000
        self.external_ip=externalip
        self.internal_ip=internalip
        self.asn=0
        self.external_network_information=external_network_information
        self.internal_network_information=internal_network_information
        self.max_unwanted_buffer_size=5000
        self.internal_is_private=internal_is_private
        self.external_is_private=external_is_private
        self.interface=interface

        self.database=database
        self.verbose=verbose
        self.os_info=""
        self.packet_number=0

        self.unwanted_packet_count=0

        self.internal_ip_randomized=self.randomize_ip(internalip)
        self.external_ip_randomized=self.randomize_ip(externalip)


    def log_local_terminal_and_GUI_WARN(self,event_string,level):
        if level >= self.verbose:
            print(event_string, flush=True)

    def check_if_common_port(self,port):
        if port< 1200:
            return True
        elif port in COMMON_PORTS:
            return True
        else:
            return False


    
    def open_port(self,local_ip,local_port,remote_ip,pkt_info):
        if local_port not in self.currently_open_ip_list:
            self.currently_open_ip_list[local_port] = set()
        # add the remote IP
        self.currently_open_ip_list[local_port].add(remote_ip)

            
    def close_port(self,local_ip,local_port,remote_ip,historical_unacked_syn):
        remotes = self.currently_open_ip_list.get(local_port)
        if not remotes:
            return

        remotes.discard(remote_ip)  # discard() is safe if not present
        if not remotes:
            # no more connections → delete key, preserving order of the rest
            del self.currently_open_ip_list[local_port]

        # still record for “previously open” logic
        self.add_port_to_previously_open(local_ip, local_port, remote_ip, historical_unacked_syn)


    def num_open_connections(self, local_port) -> int:
        """
        Number of distinct remote IPs currently connected.
        """
        return len(self.currently_open_ip_list.get(local_port, ()))    

    def num_previously_open_connections(self, local_port) -> int:
        """
        Return the number of distinct remote IPs that were previously
        open on local_port, across both A and B windows.
        """
        a = self.previously_open_ip_list_A.get(local_port, set())
        b = self.previously_open_ip_list_B.get(local_port, set())
        # union so we don’t double‐count an IP seen in both windows
        return len(a | b)

    def add_port_to_previously_open(self, local_ip, local_port, remote_ip, pkt_info):
        

        # rolling‐window switch (unchanged)
        if pkt_info.packet_time - self.previously_open_ip_list_ptr["time_started"] > \
           self.Recently_closed_port_timeout:

            tmp = (
                self.previously_open_ip_list_B
                if self.previously_open_ip_list_ptr is self.previously_open_ip_list_A
                else self.previously_open_ip_list_A
            )
            tmp.clear()
            tmp["time_started"] = pkt_info.packet_time
            self.previously_open_ip_list_ptr = tmp

        # now record the remote_ip in a set for that port
        wins = self.previously_open_ip_list_ptr
        if local_port not in wins:
            wins[local_port] = set()
        wins[local_port].add(remote_ip)




    def was_port_previously_open(self, local_ip, local_port, remote_ip, pkt_info):
        # look in both windows A and B:
        for window in (self.previously_open_ip_list_A,
                       self.previously_open_ip_list_B):
            remotes = window.get(local_port)
            if remotes and remote_ip in remotes:
                return True
        return False
        


            
    def is_port_open(self, local_ip, local_port, remote_ip):
        # Check if the local IP is present.
        if local_port in self.currently_open_ip_list :
            return True
        return False


    
    
    
    def is_ip_dst_on_local_network(self,ip_dst):
        if ip_dst==self.internal_ip or ip_dst==self.external_ip:
            return True
        else:
            return False
        
    def is_ip_src_on_local_network(self,ip_src):
        if ip_src==self.internal_ip or ip_src==self.external_ip:
            return True
        else:
            return False
    
    def add_L2_reachable_host(self,ip,MAC,current_packet):
        if not self.is_ip_dst_on_local_network(ip):
            self.currently_open_ip_list[ip]={}
            #self.log_local_terminal_and_GUI_WARN(f"ARP: Added add_L2_reachable_host {ip} based on num {current_packet.packet_num} {current_packet.packet}",4)
            justification=f"Justification: Packet Number {current_packet.packet_num}  {current_packet.packet.payload}"
            #self.gui_sock.send(f"ARP: Added add_L2_reachable_host {ip} based on num {current_packet.packet_num} {current_packet.packet}")
            
    def remove_L2_reachable_host(self,ip,MAC):
        if self.is_ip_dst_on_local_network(ip):
            #self.currently_open_ip_list.remove(ip)
            del self.currently_open_ip_list[ip]

    

    
    def print_currently_open_ports(self): 
        return
        if self.verbose ==0:
            self.log_local_terminal_and_GUI_WARN("----- Currently Open Ports -----",0)
            for ip, ports in self.currently_open_ip_list.items():
                self.log_local_terminal_and_GUI_WARN(f"IP: {ip}", 0)
                # Check if the value is a dictionary (it should be in your design)
                if isinstance(ports, dict):
                    for port, pkt_list in ports.items():
                        self.log_local_terminal_and_GUI_WARN(f"  Port: {port}", 0)
                        # Each item in pkt_list is assumed to be a Packet_info object.
                        for remote_ip in pkt_list:
                            self.log_local_terminal_and_GUI_WARN(f"    remote_ip {remote_ip}", 0)
                else:
                    # Print the value directly if it's not a dictionary.
                    self.log_local_terminal_and_GUI_WARN(f"  {ports}",0)
            self.log_local_terminal_and_GUI_WARN("----- End of Currently Open Ports -----",0)
      
           

                    
    def Remove_ARP_from_watch(self,Matching_ARP):
        for x in range(len(self.ARP_requests) - 1, -1, -1):
            historical_ARP= self.ARP_requests[x]
            if  historical_ARP.packet[ARP].pdst == Matching_ARP.packet[ARP].psrc :
                    #self.log_local_terminal_and_GUI_WARN(f"Removed answered ARP self.ARP_requests[x] {self.ARP_requests[x].packet} after {Matching_ARP.packet.time - self.ARP_requests[x].packet.time} delay"+\f" due to Matching_ARP.packet {Matching_ARP.packet} {Matching_ARP.packet.time} with {self.ARP_requests[x].packet} {self.ARP_requests[x].packet.time}",1)
                    #self.log_local_terminal_and_GUI_WARN(f"Matching_ARP.packet[ARP].psrc {Matching_ARP.packet[ARP].psrc} Matching_ARP.packet[ARP].pdst {Matching_ARP.packet[ARP].pdst} self.ARP_requests[x].packet[ARP].psrc {self.ARP_requests[x].packet[ARP].psrc} self.ARP_requests[x].packet[ARP].pdst {self.ARP_requests[x].packet[ARP].pdst}",1)
                    del self.ARP_requests[x]
                    
    
    def Check_SYN_watch(self,current_packet):
        pass

        
    def Process_ACK(self,pkt_info):
        #TODO: find the SYN and remove it before timer expires, if port closed mark as open
        self.remove_pkt_from_watch(pkt_info)
        
    def Process_Outgoing_TCP(self,pkt_info):
        if "A" in pkt_info.tcp_flags and "R" not in pkt_info.tcp_flags:
            #logging.info(f"Outgoing SA detected, so remove corresponding syn from list of unacked syns and process it as an open port{current_packet.packet}")
            #self.log_local_terminal_and_GUI_WARN(f" Process_Outgoing_TCP: Outgoing A detected, so remove corresponding pckts from list of unacked and process it as an open port",1)
            self.Process_ACK(pkt_info)
            self.open_port(pkt_info.ip_src,pkt_info.tcp_sport,pkt_info.ip_dst, pkt_info)
        if "F" in pkt_info.tcp_flags:
            #self.log_local_terminal_and_GUI_WARN(f"Process_Outgoing_TCP: Fin flag, add_port_to_previously_open(pkt_info.ip_src,pkt_info.tcp_sport,pkt_info) {pkt_info.ip_src } {pkt_info.tcp_sport} {pkt_info.ip_dst}",0)
            self.close_port(pkt_info.ip_src,pkt_info.tcp_sport,pkt_info.ip_dst,pkt_info)
            #self.add_port_to_previously_open(pkt_info.ip_src,pkt_info.tcp_sport,pkt_info.ip_dst,pkt_info)
            




    #only called if we got an ack, so we can remove all if duplicates so we error on the side of false negatives
    def remove_pkt_from_watch(self, pkt):
        key = (pkt.ip_dst, pkt.tcp_dport,pkt.ip_src, pkt.tcp_sport)
        self.packets_to_watch.pop(key, None)

    # ---------- hotpath: add packet ------------------------------------
    def add_pkt_to_watch(self, pkt):
        key = (pkt.ip_src, pkt.tcp_sport, pkt.ip_dst, pkt.tcp_dport)
        bucket = self.packets_to_watch.get(key)
        if bucket is None:              # new flow
            self.packets_to_watch[key] = [pkt]     # key goes to the end (newest)
        else:
            bucket.append(pkt)          # duplicates keep flow position

    # ---------- coldpath: reap expired ---------------------------------
    def clear_expired_pkts(self, now):

        while self.packets_to_watch:
            key, bucket = next(iter(self.packets_to_watch.items()))   # oldest flow

            # If the *oldest* packet in the oldest flow is still fresh, stop.
            if now - bucket[0].packet_time <= self.SYN_reply_timeout:
                break

            # -----------------------------------------------------------------
            # Remove ALL expired packets in *this* bucket.
            while bucket and now - bucket[0].packet_time > self.SYN_reply_timeout:
                un_acked_pkt = bucket.pop(0)
                self.Report_unwanted_traffic(un_acked_pkt, "N/A", "N/A")

            # -----------------------------------------------------------------
            if not bucket:                           # list is empty  drop key
                self.packets_to_watch.popitem(last=False)
                continue                             # check the NEW oldest bucket

            # Bucket still has newer packets: move the key to 'newest' position
            self.packets_to_watch.move_to_end(key)
            # continue  the next bucket (now the oldest) may still hold expiries

    def clear_and_report_all_watched_packets(self):
        while self.packets_to_watch:                                   # while any flow left
            key, bucket = self.packets_to_watch.popitem(last=False)    # oldest flow (O(1))
            while bucket:                                   # oldest packet first
                un_acked_pkt = bucket.pop(0)
                self.Report_unwanted_traffic(un_acked_pkt, "N/A", "N/A")




    def Clear_unreplied_ARPs(self,current_packet):
        while len(self.ARP_requests):
            if current_packet.packet.time - self.ARP_requests[0].packet.time >= self.ARP_reply_timeout :
                if self.is_ip_dst_on_local_network(self.ARP_requests[0].packet[ARP].pdst):
                    #self.log_local_terminal_and_GUI_WARN(f"ARP: Remove ip {self.ARP_requests[0].packet[ARP].pdst} from local hosts  ARP TIMEOUT: self.ARP_requests was never replied to, packet number :{self.ARP_requests[0].packet_num} {self.ARP_requests[0].packet} ",4)
                    unwanted_packet=self.ARP_requests.popleft()
                    self.remove_L2_reachable_host(unwanted_packet.packet[ARP].pdst,"")
                else:
                    #self.log_local_terminal_and_GUI_WARN(f"ARP:would remove ip {self.ARP_requests[0].packet[ARP].pdst} but it's not in local hosts. TIMEOUT: self.ARP_requests was never replied to, packet number :{self.ARP_requests[0].packet_num} {self.ARP_requests[0].packet}, ",4)
                    self.ARP_requests.popleft()

            else:
                break
    
    def Process_TCP(self,pkt_info):
        #incoming packets,we onlcy care about those to enpoints we monitor
        if self.is_ip_dst_on_local_network(pkt_info.ip_dst):
            self.num_total_tcp_packets=self.num_total_tcp_packets+1

            #self.log_local_terminal_and_GUI_WARN(f"Process_TCP: ***************** packet_num:{pkt_info.packet_num} seq:{pkt_info.tcp_seq} Incoming Seen at Process_TCP ******************",0)
            #self.log_local_terminal_and_GUI_WARN(f"Process_TCP: Incoming pkt_info.ip_src:{pkt_info.ip_src} pkt_info.ip_dst:{pkt_info.ip_dst} pkt_info.tcp_sport:{pkt_info.tcp_sport} pkt_info.tcp_dport:{pkt_info.tcp_dport} pkt_info.tcp_seq:{pkt_info.tcp_seq} ",0)
            #self.log_local_terminal_and_GUI_WARN(f"Process_TCP: ***************** {pkt_info.tcp_seq} self.print_currently_open_ports() ******************",0)
            #self.log_local_terminal_and_GUI_WARN(self.print_currently_open_ports(),0)
            #self.log_local_terminal_and_GUI_WARN(f"Process_TCP:  ***************** {pkt_info.tcp_seq} end currently_open_ports() ******************",0)

            '''if self.is_port_open(pkt_info.ip_dst,pkt_info.tcp_dport,pkt_info.ip_src):
                #self.log_local_terminal_and_GUI_WARN(f"Process_TCP: ***************** {pkt_info.tcp_seq} self.is_port_open came back true {pkt_info.ip_dst} ,{ pkt_info.tcp_dport} ",0)
                pass
            #error on side of caution, if port was previously open there's a chance packets may not be unwanted
            elif self.was_port_previously_open(pkt_info.ip_dst,pkt_info.tcp_dport,pkt_info.ip_src,pkt_info ) is True:
                #self.log_local_terminal_and_GUI_WARN(f"Process_TCP: ***************** {pkt_info.tcp_seq} self.is_port_open false, but self.was_port_previously_open came back true {pkt_info.ip_dst} ,{ pkt_info.tcp_dport} ",0)
                pass          
            else:'''
                #self.log_local_terminal_and_GUI_WARN(f"Process_TCP: ***************** {pkt_info.tcp_seq} self.was_port_previously_open came back false {pkt_info.ip_dst} ,{ pkt_info.tcp_dport} ",0)
                #strrr=self.print_previously_open_ports()
                #self.log_local_terminal_and_GUI_WARN(f"Process_TCP: entries in was_port_previously_open {strrr}",0)
            self.add_pkt_to_watch(pkt_info)          
        #outgoing packets
        elif self.is_ip_src_on_local_network(pkt_info.ip_src):
            #self.log_local_terminal_and_GUI_WARN(f"Process_TCP: ***************** packet_num:{pkt_info.packet_num} seq:{pkt_info.tcp_seq} Outgoing Seen at Process_TCP ******************",0)
            #self.log_local_terminal_and_GUI_WARN(f"Process_TCP: Outgoing pkt_info.ip_src:{pkt_info.ip_src} pkt_info.ip_dst:{pkt_info.ip_dst} pkt_info.tcp_sport:{pkt_info.tcp_sport} pkt_info.tcp_dport:{pkt_info.tcp_dport} pkt_info.tcp_seq:{pkt_info.tcp_seq} ",0)
            self.Process_Outgoing_TCP(pkt_info)
        #self.log_local_terminal_and_GUI_WARN(f"\n\n=============================\n\n",0)


    def print_previously_open_ports(self):
        if self.verbose ==0:
            strrr=""
            for outer_key  in self.previously_open_ip_list_A.keys():
                strrr+="A"+str(outer_key)+","
            for outer_key in self.previously_open_ip_list_B.keys():
                strrr+="B"+str(outer_key)+","
        
            
            #self.log_local_terminal_and_GUI_WARN(f"print_previously_open_ports: {strrr}",0)
            
        
    def hash_segment(self,segment, key):
        """
        Hash an IP segment (octet) with a key and return a consistent random value in [0, 255].
        """

        
        # Combine segment and key
        combined = f"{segment}-{key}"
        # Hash using SHA256
        hashed = hashlib.sha256(combined.encode()).hexdigest()
        # Map to a number in the range 0-255
        return int(hashed[:2], 16) % 256

    def randomize_ip(self,ip_address):
        key="LightScope123!"
        try:
            ip = ipaddress.IPv4Address(ip_address)
            octets = str(ip).split('.')
            randomized_octets = [self.hash_segment(octet, key) for octet in octets]
            randomized_ip = ".".join(map(str, randomized_octets))
            return randomized_ip
        except ipaddress.AddressValueError:
            raise ValueError("Invalid IP address format.")
                   
    def Report_unwanted_traffic(self,pkt_info,reason,confidence): 
        self.report_unwanted.append(pkt_info)
        self.num_unwanted_tcp_packets=self.num_unwanted_tcp_packets+1
        self.prepare_data(pkt_info)
       
    
                
    

    def prepare_data(self,pkt_info):
        current_open_common_ports = []
        for port, remotes in self.currently_open_ip_list.items():
            # skip non-numeric keys (like "time_started" in your prev lists) if any
            if not isinstance(port, int):
                continue
            if self.check_if_common_port(port):
                count = len(remotes)
                current_open_common_ports.append(f"{port}x{count}")

        previosuly_open_common_ports = []
        # gather all ports seen in either A or B
        all_prev_ports = set(self.previously_open_ip_list_A) | set(self.previously_open_ip_list_B)
        for port in all_prev_ports:
            if port == "time_started" or not isinstance(port, int):
                continue
            if self.check_if_common_port(port):
                # union the two sets so we count each remote IP only once
                remotes_a = self.previously_open_ip_list_A.get(port, set())
                remotes_b = self.previously_open_ip_list_B.get(port, set())
                count = len(remotes_a | remotes_b)
                previosuly_open_common_ports.append(f"{port}x{count}")

        

        payload = {
            "db_name":                        self.database,
            "system_time":                    str(pkt_info.packet_time),
            "ip_version":                     pkt_info.ip_version,
            "ip_ihl":                         pkt_info.ip_ihl,
            "ip_tos":                         pkt_info.ip_tos,
            "ip_len":                         pkt_info.ip_len,
            "ip_id":                          pkt_info.ip_id ,
            "ip_flags":                       ",".join(str(v) for v in pkt_info.ip_flags),
            "ip_frag":                        pkt_info.ip_frag,
            "ip_ttl":                         pkt_info.ip_ttl,
            "ip_proto":                       pkt_info.ip_proto,
            "ip_chksum":                      pkt_info.ip_chksum,
            "ip_src":                         pkt_info.ip_src,
            "ip_dst_randomized":              self.randomize_ip(pkt_info.ip_dst),
            "ip_options":                     ",".join(str(v) for v in pkt_info.ip_options ),
            "tcp_sport":                      pkt_info.tcp_sport,           
            "tcp_dport":                      pkt_info.tcp_dport,           
            "tcp_seq":                        pkt_info.tcp_seq ,            
            "tcp_ack":                        pkt_info.tcp_ack ,            
            "tcp_dataofs":                    pkt_info.tcp_dataofs ,        
            "tcp_reserved":                   pkt_info.tcp_reserved,   
            "tcp_flags":                      pkt_info.tcp_flags,
            "tcp_window":                     pkt_info.tcp_window,
            "tcp_chksum":                     pkt_info.tcp_chksum,
            "tcp_urgptr":                     pkt_info.tcp_urgptr,
            "ext_dst_ip_country":             self.external_network_information[0],
            "ext_dst_ip_net_type":            self.external_network_information[1],
            "ext_asn":                        self.external_network_information[2],
            "int_dst_ip_country":             self.internal_network_information[0],
            "int_dst_ip_net_type":            self.internal_network_information[1],
            "int_asn":                        self.internal_network_information[2],
            "internal_is_private":            self.internal_is_private,
            "external_is_private":            self.external_is_private,
            "open_ports":                     ",".join(current_open_common_ports), 
            "previously_open_ports":          ",".join(previosuly_open_common_ports),        
            "tcp_options":                    ",".join(str(v) for v in pkt_info.tcp_options ),
            "interface":                      self.interface,
            "internal_ip_randomized":         self.internal_ip_randomized,
            "external_ip_randomized":         self.external_ip_randomized
        }

        self.report_output_buffer.send(payload)
        self.unwanted_packet_count=self.unwanted_packet_count+1
        #if self.unwanted_packet_count % 1000 ==0:
            #self.log_local_terminal_and_GUI_WARN(f"self.unwanted_packet_count {self.unwanted_packet_count}",0)

 


    def ARP_add_hosts(self,current_packet):
        #logging.info(f"AAAAAAAAAAAAAAA current_packet.packet[ARP] {current_packet.packet[ARP].show(dump=True)}")
        #logging.warning(f"AAAAAAAAAAAAAAA  {dir(current_packet.packet[ARP])}")
        self.add_L2_reachable_host(current_packet.packet[ARP].psrc,current_packet.packet[ARP].hwsrc,current_packet)
        
    
    def ARP_add_request_watch(self,current_packet):
        #Track the ARP request, if it goes unanswered remove the requested host from L2 reachable
        #current_packet.packet[ARP].op == 2 means it was an ARP reply, ==1 is a request
        matching_out_of_order_reply=0
        self.ARP_same_timestamp.append(current_packet)
        if self.ARP_same_timestamp[0].packet.time != current_packet.packet.time:
            self.ARP_same_timestamp.clear()
            self.ARP_same_timestamp.append(current_packet)
        else:
            self.ARP_same_timestamp.append(current_packet)
        
        if current_packet.packet[ARP].op == 1:
            if self.ARP_same_timestamp:
                if self.ARP_same_timestamp[0].packet.time == current_packet.packet.time:
                    for ARP_with_same_timestamp in self.ARP_same_timestamp:
                        if  current_packet.packet[ARP].pdst == ARP_with_same_timestamp.packet[ARP].psrc :
                            matching_out_of_order_reply=1
                            #self.log_local_terminal_and_GUI_WARN(f"Out of order ARP reply for num {current_packet.packet_num} {current_packet.packet} and {ARP_with_same_timestamp.packet_num} {ARP_with_same_timestamp.packet} ",1)  
                if not matching_out_of_order_reply:
                    self.ARP_requests.append(current_packet)
            
    

                    
    def Process_ARP(self,current_packet):
        #if collecting on all IPs use ARP method
        pass
        '''if self.collection_ip == "all":
            if current_packet.packet.haslayer(ARP):# 
                #Add the sender of the ARP request, we know they are there
                self.ARP_add_hosts(current_packet)
                self.ARP_add_request_watch(current_packet)
                #TODO: maybe change logic here to detect MAC issues with ip addresses and ARP, for now if it's responding/originating ARP then you can remove unreplied ARPs
                self.Clear_unreplied_ARPs(current_packet)
                self.Remove_ARP_from_watch(current_packet)'''
            
    
        
      
        
    def Process_packet(self,pkt_info):
        self.Process_ARP(pkt_info)
        self.Process_TCP(pkt_info)
        

    def ensure_directory(self,directory_name):
        """Ensure the directory exists, and if not, create it."""
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)



    def packet_handler(self, unprocessed_packets):
        '''bechmark_list=[]
        while True:
            # 1) wait up to self.SYN_reply_timeout for the next batch, if it takes longer than that you can clear all the packets from the watch, they didn't get acked in time
            if unprocessed_packets.poll(self.SYN_reply_timeout):
                try:
                    batch = unprocessed_packets.recv()   # Handler got a real batch
                except (EOFError, OSError):
                    # Pipe was closed or broken
                    break

                # 2) process it
                bechmark_list.append(batch)

                # 3) ACK back to capture
                try:
                    unprocessed_packets.send(None)
                except (BrokenPipeError, EOFError, OSError):
                    break'''


        """
        Receives batches over a duplex Pipe with a timeout. If no batch
        arrives in TIMEOUT seconds, clear & report *all* watched packets.
        """

        while True:
            # 1) wait up to self.SYN_reply_timeout for the next batch, if it takes longer than that you can clear all the packets from the watch, they didn't get acked in time
            if unprocessed_packets.poll(self.SYN_reply_timeout):
                try:
                    batch = unprocessed_packets.recv()   # Handler got a real batch
                except (EOFError, OSError):
                    # Pipe was closed or broken
                    break

                # 2) process it
                for pkt in batch:
                    self.Process_packet(pkt)
                self.clear_expired_pkts(batch[-1].packet_time)

                # 3) ACK back to capture
                try:
                    unprocessed_packets.send(None)
                except (BrokenPipeError, EOFError, OSError):
                    break

            else:
                # 4) timeout expired  no new packets in TIMEOUT
                #    flush everything still being watched
                self.clear_and_report_all_watched_packets()
                # then loop back and poll() again
                    


        
        

from collections import deque
import time
import requests
from requests.adapters import HTTPAdapter

def send_data(consumer_upload_conn):
    API_URL = "https://lightscope.isi.edu/log_mysql_data"
    HEADERS = {
        "Content-Type":  "application/json",
        "X-API-Key":     "lightscopeAPIkey2025_please_dont_distribute_me_but_im_write_only_anyways"
    }
    BATCH_SIZE     = 600
    IDLE_FLUSH_SEC = 5.0    # send whatever is left every 5s even if < BATCH_SIZE
    RETRY_BACKOFF  = 5      # seconds to wait on failure

    session = requests.Session()
    adapter = HTTPAdapter(pool_connections=4, pool_maxsize=4)
    session.mount("https://", adapter)
    session.mount("http://", adapter)

    queue = deque()
    last_activity = time.monotonic()
    stop_event = threading.Event()

    # --------------------------- reader thread ---------------------------
    def reader():
        nonlocal last_activity
        while not stop_event.is_set():
            try:
                # block until an item arrives (or EOF)
                item = consumer_upload_conn.recv()
            except (EOFError, OSError):
                stop_event.set()
                break
            queue.append(item)
            last_activity = time.monotonic()
        # drain any remaining items
        while True:
            try:
                item = consumer_upload_conn.recv_nowait()
            except Exception:
                break
            queue.append(item)

    t = threading.Thread(target=reader, daemon=True)
    t.start()

    # --------------------------- flush loop ---------------------------
    try:
        while not stop_event.is_set() or queue:
            now = time.monotonic()
            elapsed = now - last_activity

            # decide if it's time to flush
            if queue and (len(queue) >= BATCH_SIZE or elapsed >= IDLE_FLUSH_SEC):
                to_send = min(len(queue), BATCH_SIZE)
                batch = [queue.popleft() for _ in range(to_send)]
                try:
                    resp = session.post(
                        API_URL,
                        json={"batch": batch},
                        headers=HEADERS,
                        timeout=10,
                        verify=False
                    )
                    

                    if resp.status_code != 200:
                        # Log the full response so you can see the error message
                        print("Server rejected payload:", resp.status_code, resp.text, flush=True)
                    print(f"Flushed {to_send} items", flush=True)
                    last_activity = time.monotonic()

                    resp.raise_for_status()

                except requests.RequestException as e:
                    # Re-queue the failed batch at front
                    print("Upload error, will retry batch:", e, flush=True)
                    for item in reversed(batch):
                        queue.appendleft(item)
                    # back off before retrying
                    time.sleep(RETRY_BACKOFF)
                    last_activity = time.monotonic()
            else:
                # avoid busy-wait
                time.sleep(0.1)
    finally:
        stop_event.set()
        t.join()




                
def read_from_interface_mac_linux(network_interface,
                        unprocessed_packets,         # duplex Pipe
                        promisc_mode=False):

    import pylibpcap.base
    BATCH_SIZE      = 280
    IDLE_FLUSH_SECS = 1.0
    SLEEP_DELAY     = 0.001  # 1ms when no flush condition met
    send_deque   = deque()
    last_activity = time.monotonic()

    # --------------------------- sender thread ---------------------------
    def sender_thread():
        nonlocal last_activity
        
        #todo remove debug

        prior_time=time.monotonic()
        packets_processed=0

        

        while True:
            now = time.monotonic()
            to_send = 0

            if (now - prior_time) >= IDLE_FLUSH_SECS:
                print(f"sender_thread: len(send_deque) {len(send_deque)} pps {packets_processed}",flush=True)
                packets_processed=0
                prior_time=now



            # 1) full batch ready?
            if len(send_deque) >= BATCH_SIZE:
                to_send = BATCH_SIZE

            # 2) idle timeout expired & buffer non-empty?
            elif send_deque and (now - last_activity) >= IDLE_FLUSH_SECS:
                to_send = len(send_deque)

            # 3) nothing to do right now
            else:
                time.sleep(SLEEP_DELAY)
                continue

            
            '''#TODO remove
            import pickle, statistics
            samples = [pickle.dumps(pkt) for pkt in send_deque]
            avg = statistics.mean(len(s) for s in samples)
            print("~", avg, "bytes per PacketInfo")'''
            
            
            # build and send batch
            batch = [send_deque.popleft() for _ in range(to_send)]
            try:
                unprocessed_packets.send(batch)       # send to handler
            except Exception as e:
                print("pipe send error:", e, file=sys.stderr)
                return



            #todo remove debug code
            packets_processed+=to_send

            # wait for ACK before next batch
            try:
                unprocessed_packets.recv()            # handler must send something back
            except Exception as e:
                print("pipe recv (ACK) error:", e, file=sys.stderr)
                return

    threading.Thread(target=sender_thread, daemon=True).start()

    # --------------------------- sniffer init ----------------------------
    try:
        sniffobj = pylibpcap.base.Sniff(
            network_interface,
            count=-1,
            promisc=int(promisc_mode),
            #todo may need to allow ARP again if discovering
            filter="ip and tcp",
            buffer_size=1 << 20,
            snaplen=256
        )
    except Exception as e:
        print(f"ERROR initializing capture: {e}", file=sys.stderr)
        sys.exit(1)

    # --------------------------- capture loop ---------------------------
    packet_number = 0
    for plen, ts, buf in sniffobj.capture():
        packet_number += 1
        try:
            try:
                pkt_info = parse_packet_info_fast(buf, packet_number)
            except Exception:
                pkt_info = parse_packet_info(buf, packet_number)
        except Exception:
            # could be VLAN, ARP, IPv6, malformedjust drop it
            continue

        send_deque.append(pkt_info)
        last_activity = time.monotonic()


import sys
import time
import threading
from collections import deque



def read_from_interface_windows(network_interface,
                                unprocessed_packets,  # duplex Pipe
                                promisc_mode=False):
    import pcap
    # --- 1) Discover all raw NPF device names ---
    devs = pcap.findalldevs()
    if not devs:
        print("No capture devices found. Is Npcap installed and running?", file=sys.stderr)
        sys.exit(1)

    # If the caller passed a friendly name (e.g. "Ethernet"), try to match it:
    if network_interface not in devs:
        print(f"Warning: '{network_interface}' is not one of the NPF devices.", file=sys.stderr)
        print("Available devices:", file=sys.stderr)
        for i, d in enumerate(devs, 1):
            print(f"  {i}. {d}", file=sys.stderr)
        # fall back to first device
        network_interface = devs[0]
        print(f"Falling back to first device: {network_interface!r}", file=sys.stderr)

    BATCH_SIZE      = 280
    IDLE_FLUSH_SECS = 1.0
    SLEEP_DELAY     = 0.001  # 1ms when no flush condition met
    send_deque      = deque()
    last_activity   = time.monotonic()

    # --------------------------- sender thread ---------------------------
    def sender_thread():
        nonlocal last_activity
        prior_time = time.monotonic()
        packets_processed = 0

        while True:
            now = time.monotonic()
            to_send = 0

            if (now - prior_time) >= IDLE_FLUSH_SECS:
                print(f"sender_thread: len(send_deque) {len(send_deque)} pps {packets_processed}", flush=True)
                packets_processed = 0
                prior_time = now

            if len(send_deque) >= BATCH_SIZE:
                to_send = BATCH_SIZE
            elif send_deque and (now - last_activity) >= IDLE_FLUSH_SECS:
                to_send = len(send_deque)
            else:
                time.sleep(SLEEP_DELAY)
                continue

            batch = [send_deque.popleft() for _ in range(to_send)]
            try:
                unprocessed_packets.send(batch)
            except Exception as e:
                print("pipe send error:", e, file=sys.stderr)
                return

            packets_processed += to_send
            try:
                unprocessed_packets.recv()
            except Exception as e:
                print("pipe recv (ACK) error:", e, file=sys.stderr)
                return

    threading.Thread(target=sender_thread, daemon=True).start()

    # --------------------------- sniffer init ----------------------------
    try:
        sniffer = pcap.pcap(
            name=network_interface,
            snaplen=256,
            promisc=bool(promisc_mode),
            immediate=True,
            timeout_ms=50
        )
    except Exception as e:
        print(f"ERROR initializing capture: {e}", file=sys.stderr)
        sys.exit(1)

    # --- verify it really opened ---
    linktype = sniffer.datalink()
    if linktype < 0:
        print(f"ERROR: Failed to open '{network_interface}' (datalink() returned {linktype})", file=sys.stderr)
        sys.exit(1)

    # --- install the BPF filter ---
    try:
        sniffer.setfilter("ip and tcp")
    except Exception as e:
        print(f"ERROR setting filter: {e}", file=sys.stderr)
        sys.exit(1)

    # --------------------------- capture loop ----------------------------
    packet_number = 0
    for ts, buf in sniffer:
        packet_number += 1
        try:
            try:
                pkt_info = parse_packet_info_fast(buf, packet_number)
            except Exception:
                pkt_info = parse_packet_info(buf, packet_number)
        except Exception:
            continue

        send_deque.append(pkt_info)
        last_activity = time.monotonic()



import re

def fix_npf_name(s: str) -> str:
    # 1) collapse '\\'  '\'
    s = s.replace('\\\\', '\\')
    # 2) collapse '{{GUID}}'  '{GUID}'
    return re.sub(r'\{\{(.*?)\}\}', r'{\1}', s)

def is_npcap_installed():
            try:
                import ctypes
                # Attempt to load both DLLs
                ctypes.WinDLL("wpcap.dll")
                ctypes.WinDLL("Packet.dll")
                return True
            except OSError:
                return False
            
def choose_windows_interface():
    
    if not is_npcap_installed():
        print(f"\n\n\n**Error detected*** \n",flush=True)
        print(f"In order to run LightScope on Windows (other Operating systems don't need to do this), you need to first install Npcap, which can be found here! https://npcap.com/#download",flush=True)
        print(f"Please choose Npcap 1.81 installer for Windows 7/2008R2, 8/2012, 8.1/2012R2, 10/2016, 2019, 11 (x86, x64, and ARM64).",flush=True)
        print(f"When installing, make sure you select Install Npcap in WinPcap API-compatible Mode. This should be selected by default.",flush=True)
        print(f"\n***Exiting***\n",flush=True)
        sys.exit()
        # exit or raise as needed
    else:
        print("Npcap is installed and available on Windows!")

    import wmi
    c = wmi.WMI()
    adapters = []
    for nic in c.Win32_NetworkAdapter():
        if nic.GUID:  # skip adapters without a GUID
            npf_name = rf"\\Device\\NPF_{{{nic.GUID}}}"
            friendly = nic.Name or nic.Description or "<Unknown>"
            adapters.append((npf_name, friendly))

    # 2) Present the list to the user
    for i, (npf, friendly) in enumerate(adapters, start=1):
        print(f"{i}. {friendly} ({npf})")

    # 3) Let the user choose
    choice = int(input("Pick an interface: ")) - 1
    chosen_npf = adapters[choice][0]
    chosen_npf =fix_npf_name(chosen_npf)
    print(f"chosen_npf {chosen_npf}",flush=True)
    return chosen_npf

def choose_mac_linux_interface():
    import socket
    raw = socket.if_nameindex()
    devs = [name for (_, name) in raw]
    if not devs:
        print("No network interfaces found!", file=sys.stderr)
        sys.exit(1)

    print("Available interfaces:")
    for i, name in enumerate(devs, start=1):
        print(f"  {i}. {name}")

    # Prompt user
    while True:
        choice = input(f"Pick an interface [1-{len(devs)}]: ").strip()
        if not choice:
            idx = 0
            break
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(devs):
                break
        print("Invalid selection, try again.")

    return devs[idx]



def lightscope_run():

    unprocessed_packets_consumer, unprocessed_packets_producer = multiprocessing.Pipe(duplex=True)

    '''# For packets that need to be processed
    consumer_packet_conn, producer_packet_conn  = multiprocessing.Pipe(duplex=False)

    # For packet_process_status
    consumer_status_conn, producer_status_conn  = multiprocessing.Pipe(duplex=False)'''

    #choose interface
    if  platforminfo.system() == "Windows":
        network_interface=choose_windows_interface()
    else:
        network_interface=choose_mac_linux_interface()


    #ELSE NOT WINDOWS HACK



    # For data to be uploaded
    consumer_upload_conn, producer_upload_conn = multiprocessing.Pipe(duplex=False)

    #todo: if ip changes just delete and recreate lightscope object, all watched packets should be dropped because we never would know if unwanted or not

    config_reader=configuration_reader()
    #network_interface=config_reader.pre_run_setup()

    Port_status=Ports(producer_upload_conn,config_reader.internal_ip,config_reader.external_ip,config_reader.verbose,config_reader.database,\
        config_reader.internal_is_private,config_reader.external_is_private,config_reader.internal_ip_equals_external_ip,network_interface,\
        config_reader.external_network_information,config_reader.internal_network_information)    
    
    
    upload_process= multiprocessing.Process(target=send_data,args=(consumer_upload_conn,))
    upload_process.start()

    lightscope_process= multiprocessing.Process(target=Port_status.packet_handler,args=(unprocessed_packets_consumer,))
    lightscope_process.start()


    if  platforminfo.system() == "Windows":
        read_from_interface_process=multiprocessing.Process(target=read_from_interface_windows,args=(network_interface,unprocessed_packets_producer,))
    else:
        read_from_interface_process=multiprocessing.Process(target=read_from_interface_mac_linux,args=(network_interface,unprocessed_packets_producer,))
    
    read_from_interface_process.start()

    print(f"To view your logs, please visit XXXXXXXXXXXXXXXXXXXXXXXXXXX todo for report")

    #self.Shutdown_cleanup()
    read_from_interface_process.join()
    lightscope_process.join()
    upload_process.join()



class configuration_reader:
    def __init__(self, config_file='config.ini'):
        # Default values
        #this is the value in the config file
        self.collection_ip=""
        self.external_ip=""
        self.internal_ip=""
        self.interface = False
        self.gui = False
        self.verbose = 6
        self.pcap = False
        self.database = False
        self.readfile = ""
        self.internal_ip_equals_external_ip=""
        self.internal_is_private=""
        self.external_is_private=""
        self.interface=""

        self.internal_ip=""
        self.external_ip=""
        self.external_network_information=["uninitialized","uninitialized","uninitialized"]
        self.internal_network_information=["uninitialized","uninitialized","uninitialized"]
    
        
        self.self_telnet_and_ssh_honeypot_ports_to_forward=[]
        self.osinfo=""
        self.lookup_network_information_list={}
        
        # Load values from the config file.
        self.load_config(config_file)

        self.pre_run_setup()
        self.initialize_config("config.ini")
        self.print_args()


    
    def load_config(self, config_file):

        config = configparser.ConfigParser()
        config.read(config_file)
        # Assuming all configuration is under the [Settings] section.
        if 'Settings' in config:
            self.verbose = config.getint('Settings', 'verbose', fallback=self.verbose)
            self.database = config.get('Settings', 'database', fallback=self.database).lower()
            self.collection_ip=config.get('Settings', 'collection_ip', fallback="all").lower()
            self.self_telnet_and_ssh_honeypot_ports_to_forward=config.get('Settings', 'self_telnet_and_ssh_honeypot_ports_to_forward', fallback=[])
        else:
            print("Warning: 'Settings' section not found in the config file.")

    def print_args(self):
        return (f"GUI mode enabled: {self.gui}\n"

                f"Verbose level: {self.verbose} (6 is silent, 5 is unwanted traffic only, "
                f"4 includes local hosts discovered, 3 includes ports opened and closed, ... 0 is everything)\n"
                f"Remote database selected? {self.database}\n"
                f"Read File selected? {self.readfile}\n"
                f"Interface {self.interface}\n"
                f"Forwarding ports from this machine {self.self_telnet_and_ssh_honeypot_ports_to_forward} to honeypot \n"
                f"Collecting from IPs {self.collection_ip}\n")



    def update_ip_and_interface(self):
        while True:
            time.sleep(600)
            print("Timer thread",flush=True)
            self.check_if_internal_ip_changed()
            self.get_internal_host_ip()
            self.interface=self.get_interface_name(self.internal_ip)
            self.update_internal_external_ip()
            print(f"collecting on interface {self.interface}, with internal IP address {self.internal_ip} and external ip address {self.external_ip}",flush=True)
            #print(f"self.currently_open_ip_list {self.currently_open_ip_list}",flush=True)


                
    def initialize_config(self,config_file):
        # Create a ConfigParser object and read the file (if it exists)
        
        config = configparser.ConfigParser()
        if os.path.exists(config_file):
            config.read(config_file)
        else:
            # If the file doesn't exist, create it with a default [Settings] section.
            config.add_section('Settings')

        # Ensure the "Settings" section exists.
        if not config.has_section('Settings'):
            config.add_section('Settings')

        # Check for the 'database' option. If it does not exist or is empty, generate one.
        # Check for the 'database' option.
        if 'database' not in config['Settings'] or not config['Settings']['database'].strip():
            info = {
                # "System": platforminfo.system(),
                # "Node Name": platforminfo.node(),  # omitted in this example
                # "Release": platforminfo.release(),
                "Version": platforminfo.version(),
                "Machine": platforminfo.machine(),
                "Total Memory": f"{psutil.virtual_memory().total / (1024 ** 3):.2f} GB",
            }
            parts = []
            for key, value in info.items():
                # Replace any non-word characters with underscores and prefix with an 'X'
                value_safe = re.sub(r'\W+', '_', str(value).lower())
                value_safe=value_safe[:20]
                parts.append(f"X{value_safe}")
    
            # Join the parts with underscores to form a prefix
            prefix = "_".join(parts).strip('_')
    
            max_mysql_table_name_length=64
            min_random_length=16
            # Ensure the prefix is not too long so that we always have at least min_random_length for the random part.
            max_prefix_length = max_mysql_table_name_length - min_random_length
            if len(prefix) > max_prefix_length:
                prefix = prefix[:max_prefix_length]
    
            # Calculate the random part length (it will make the table name exactly max_mysql_table_name_length characters long)
            random_part_length = max_mysql_table_name_length - len(prefix)
    
            # Generate the random string from lowercase letters.
            random_db = ''.join(random.choices(string.ascii_lowercase, k=random_part_length))
    
            table_name = prefix + random_db
            config['Settings']['database'] = table_name
            print(f"Database not found; generated random database name: {table_name}")
    
        # Set defaults for the other required options if they are missing
        if 'verbose' not in config['Settings'] or not config['Settings']['verbose'].strip():
            config['Settings']['verbose'] = '6'
        if 'collection_ip' not in config['Settings'] or not config['Settings']['collection_ip'].strip():
            config['Settings']['collection_ip'] = 'self'

        # Optionally, you can also add the comment as a separate step manually 
        # (Comments are not preserved automatically by configparser when writing back.)
        # Write the configuration back to the file.
        with open(config_file, 'w') as f:
            config.write(f)
        print(f"Configuration updated and saved to {config_file}")
            
    def pre_run_setup(self):
        self.get_internal_host_ip()
        self.interface=self.get_interface_name(self.internal_ip)
        self.update_internal_external_ip()
        print(f"collecting on interface {self.interface}, with internal IP address {self.internal_ip} and external ip address {self.external_ip}",flush=True)
        #print(f"self.currently_open_ip_list {self.currently_open_ip_list}",flush=True)

        t = threading.Thread(target=self.update_ip_and_interface)
        t.start()

        return self.interface


    def check_if_internal_ip_changed(self):
        #TODO change this to match other changes to open ports
        #this solution wont work with all mode, only for self, need to update
        current_internal_ip=self.get_internal_host_ip()
        if self.internal_ip !=current_internal_ip:
            self.internal_ip =current_internal_ip
            #self.currently_open_ip_list.clear()
        return self.internal_ip


    
    def get_internal_host_ip(self):
        if self.collection_ip == "self" or self.collection_ip == "all":
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                # Connect to an external IP address (Google DNS) on port 80.
                s.connect(('8.8.8.8', 80))
                ip = s.getsockname()[0]
            except Exception:
                ip = '127.0.0.1'
            finally:
                s.close()
            self.internal_ip=ip



            #todo: change since the update to how open ports are stored
            '''if self.internal_ip not in self.currently_open_ip_list:
                self.currently_open_ip_list[ip]={}'''
            return ip
        else:
            self.internal_ip=self.collection_ip
            '''if self.internal_ip not in self.currently_open_ip_list:
                self.currently_open_ip_list[self.internal_ip]={}'''
            return self.collection_ip
    
    def get_interface_name(self,ip_address):
    # Iterate over all network interfaces and their addresses.
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET and addr.address == ip_address:
                    return interface
        return None

    def update_internal_external_ip(self):
        response = requests.get("https://ipinfo.io/what-is-my-ip")
        response=response.json()
        self.external_ip=response["ip"]
        print(f"external IP found {self.external_ip}" ,flush=True)
        self.update_internal_network_information(self.internal_ip)
        self.update_external_network_information(self.external_ip)
        self.external_is_private=self.check_ip_is_private(self.external_ip)
        self.internal_is_private=self.check_ip_is_private(self.internal_ip)
        self.internal_ip_equals_external_ip = self.external_ip == self.internal_ip



    def update_external_network_information(self,external_ip):
        self.external_network_information=self.lookup_network_information(external_ip)
        print(f"external_network_information found {self.external_network_information}" ,flush=True)


    def update_internal_network_information(self,internal_ip):
        self.internal_network_information=self.lookup_network_information(internal_ip)
        print(f"internal_network_information found {self.internal_network_information}" ,flush=True)


    def ip_to_int(self,ip_str):
        return int(ipaddress.ip_address(ip_str))

    def find_file_for_second_octet(self,directory, second_octet,ip_str):
        # List all .txt files in the directory
        files = [f for f in os.listdir(directory) if f.endswith('.txt')]
        # Extract the start octets
        starts = []
        for filename in files:
            base = os.path.splitext(filename)[0]
            try:
                start_val = int(base)
                starts.append(start_val)
            except ValueError:
                # Skip files that don't follow the naming convention
                continue

        # Sort the start values
        starts.sort()
        # Use binary search to find the file that covers this second_octet
        pos = bisect.bisect_right(starts, second_octet) - 1
        if pos < 0:
            # No start <= second_octet
            self.lookup_network_information_list[ip_str]=("error", "No start <= second_octet")
            return ("error", "No start <= second_octet","None")

        chosen_start = starts[pos]
        return os.path.join(directory, f"{chosen_start}.txt")

    def lookup_network_information(self,ip_str, base_dir="hierarchical_IP_tree"):
        ip_str=str(ip_str)
        if ip_str in self.lookup_network_information_list:
            return self.lookup_network_information_list[ip_str]

        parts = ip_str.split('.')
        if len(parts) != 4:
            self.lookup_network_information_list[ip_str]=("error", "Invalid IPv4 address 4 parts")
            return ("error", "Invalid IPv4 address 4 parts","None")
        try:
            first_octet = int(parts[0])
            second_octet = int(parts[1])
        except ValueError:
            self.lookup_network_information_list[ip_str]=("error", "Invalid IPv4 address octets")
            return ("error", "Invalid IPv4 address octets","None")

        # Construct the directory for the first octet
        first_octet_dir = os.path.join(base_dir, str(first_octet))
        if not os.path.isdir(first_octet_dir):
            # No directory for this first octet
            self.lookup_network_information_list[ip_str]=("error", "No directory for this first octet")
            return ("error", "first octet filepath","None")

        # Find the appropriate file for the second octet
        file_path = self.find_file_for_second_octet(first_octet_dir, second_octet,ip_str)
        if file_path is None or not os.path.exists(file_path):
            # No file for this second octet range
            self.lookup_network_information_list[ip_str]=("error", "second octet filepath")
            return ("error", "second octet filepath","None")

        lookup_network_information_int = self.ip_to_int(ip_str)

        # Search within this file's ranges
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts_line = line.split(',')
                if len(parts_line) < 5:
                    continue
                start_ip_str, end_ip_str, net_type, country, asn = parts_line[0], parts_line[1], parts_line[2], parts_line[3], parts_line[4]

                try:
                    start_ip_int = self.ip_to_int(start_ip_str)
                    end_ip_int = self.ip_to_int(end_ip_str)
                except ValueError:
                    # Skip invalid IP
                    continue

                if start_ip_int <= lookup_network_information_int <= end_ip_int:
                    self.lookup_network_information_list[ip_str]=(net_type, country,asn)
                    return (net_type, country,asn)


        self.lookup_network_information_list[ip_str]=("None", "IP not in dataset")
        return ("None", "IP not in dataset","None")


    def check_ip_is_private(self,ip_str):
        try:
            # Create an IP address object (works for both IPv4 and IPv6)
            ip_obj = ipaddress.ip_address(ip_str)
        
            if ip_obj.is_private:
                return(f"True")
            else:
                return(f"False")
        except ValueError:
            return(f" is not a valid IP address.")

def main():
    #profiler.enable()
    print("Welcome to lightscope!")
    lightscope_run() 
    

import cProfile
import pstats
import io
import signal
import sys
import time

'''profiler = cProfile.Profile()

def signal_handler(sig, frame):
    # Stop profiling when the signal is received
    profiler.disable()

    # Create a stream to capture the profiling output
    s = io.StringIO()
    # Configure pstats.Stats to sort by cumulative time (you can change 'cumtime' to another sort option if desired)
    ps = pstats.Stats(profiler, stream=s).sort_stats('cumtime')
    # Print the stats to our stream
    ps.print_stats()

    # Print the profiling output
    print("\n=== Profiling stats ===")
    print(s.getvalue())

    # Optionally, dump the stats to a file
    with open("profile_results.txt", "w") as f:
        f.write(s.getvalue())

    sys.exit(0)

# Register the signal handler to catch SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, signal_handler)

def run_profiled():
    profiler = cProfile.Profile()
    profiler.enable()
    main()  # run your program
    profiler.disable()

    # Create a stream for printing the stats
    s = io.StringIO()
    ps = pstats.Stats(profiler, stream=s).sort_stats("cumtime")
    ps.print_stats()
    print(s.getvalue()) '''

if __name__ == '__main__':
    main()






      


# -*- coding: utf-8 -*-
"""
Created on Thu May 12 20:30:53 2022

@author: dongo
"""

import dpkt
import datetime
from dpkt.utils import mac_to_str, inet_to_str
from dpkt.ip import IP, IP_PROTO_UDP
from dpkt.udp import UDP
import time
from numpy import savetxt
import scipy.stats
import matplotlib.pyplot as plt


def print_packets(pcap):
    """Print out information about each packet in a pcap
       Args:
           pcap: dpkt pcap reader object (dpkt.pcap.Reader)
    """
    numPackets = 0;
    lengthPackets = [];
    time1 = 0;
    time2 = 0;
    timeArr = [];

    # For each packet in the pcap process the contents
    for timestamp, buf in pcap:
        # Unpack the Ethernet frame (mac src/dst, ethertype)
        eth = dpkt.ethernet.Ethernet(buf)

        # Make sure the Ethernet data contains an IP packet
        # Now access the data within the Ethernet frame (the IP packet)
        ip = eth.data
        pp = eth.data.data

        # Grab data by UDP

        # print(ip.p)
        # Grab data by port number 8801 = zoom

        # Print out the timestamp in UTC
        time1 = datetime.datetime.utcfromtimestamp(timestamp)
        tt = time1.strftime('%H:%M:%S.%f')[:-4]

        # print('Arrival Time: ', str(tt))

        # Finding interarrival time
        numPackets += 1
        if (numPackets > 1):
            interArrival = (time1 - time2).total_seconds()
            timeArr.append(interArrival)

        # Payload size in bytes
        length = len(pp) - 8  # UDP header is 8 bytes
        lengthPackets.append(length)

        time2 = datetime.datetime.utcfromtimestamp(timestamp)
        proto = ip.get_proto(ip.p).__name__
        print(proto)
    print(numPackets)

    return lengthPackets, timeArr


def test():
    """Open up a test pcap file and print out the packets"""
    with open('captures/HTTPCapture.pcap', 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        payloadSize, interArrival = print_packets(pcap)
        savetxt('payload.csv', payloadSize, delimiter=',')
        savetxt('interarrivalTime.csv', interArrival, delimiter=',')


if __name__ == '__main__':
    test()
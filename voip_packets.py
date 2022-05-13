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
        if not isinstance(eth.data, dpkt.ip.IP):
            print('Non IP Packet type not supported %s\n' % eth.data.__class__.__name__)
            continue

        # Now access the data within the Ethernet frame (the IP packet)
        ip = eth.data
        pp = eth.data.data

        # Grab data by UDP
        if (ip.p == dpkt.ip.IP_PROTO_UDP):
            # Grab data by port number 8801 = zoom
            if (pp.sport == 8801 or pp.dport == 8801):

                # Print out the timestamp in UTC
                time1 = datetime.datetime.utcfromtimestamp(timestamp)
                tt = time1.strftime('%H:%M:%S.%f')[:-4]

                # Finding interarrival time
                if (numPackets > 1):
                    interArrival = (time1 - time2).total_seconds()
                    timeArr.append(interArrival)

                # Payload size in bytes
                length = len(pp) - 8  # UDP header is 8 bytes
                lengthPackets.append(length)

                numPackets += 1
                time2 = datetime.datetime.utcfromtimestamp(timestamp)

    return lengthPackets, timeArr


def test():
    """Open up a test pcap file and print out the packets"""
    with open('data/zoom_packets.pcap', 'rb') as f:
        pcap = dpkt.pcap.Reader(f)
        payloadSize, interArrival = print_packets(pcap)
        savetxt('payload.csv', payloadSize, delimiter=',')
        savetxt('interarrivalTime.csv', interArrival, delimiter=',')


if __name__ == '__main__':
    test()
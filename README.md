# ECE158B -- Project 1 -- Topic 1
## William Lynch A14588777 -- Dong On A15491340
---

### Overview

For our project we chose to do Topic 1, where we'll be capturing HTTP, FTP, VoIP and BitTorrent packets and analyzing their arrival time and payload size using the dpkt file parser library.  We analyzed our data by plotting the CDF and PDF of the inter-arrival time and payload sizes.

---

### Methodology

We began by capturing our packets for each of the protocols.  Firstly, we captured HTTP by accessing GNU.org, which actually as of writing this is now a secured HTTPS website.  To get FTP we accessed the FTP server at brown.edu.  For VoIP we recorded the UDP packets going back and forth while we talked to eachother across Zoom.  To get the BitTorrent packets we installed qBitTorrent on our Ubunutu VM because windows 10 blocks any torrent client from being used.  We then downloaded royalty free content.

After we captured our packets we needed to parse them out.  This proved to be difficult to do when it came to parsing by protocols that were not in the dpkt register of protocols.  This register did not include FTP, BitTorrent or HTTP.  For these captures, we filtered them out in wireshark and then exported only the displayed packets. So ultimately we had .pcap files that only included the protocols we wished to view.  This made it easier for us to parse the payload size and inter arrival time because we did not need to check if the packets were our desired protocol.  


| ![Image Caption](images/bittorrentsnip.PNG) | ![Image Caption](images/ftpsnip.PNG) |
|----|----|
| ![Image Caption](images/httpsnip.PNG) | ![Image Caption](images/voipsnip.PNG) |


VoIP was done differently however, we filterd in python by the UDP port of Zoom used during our call. We are calculating arrival time within this chunk of code as well as filtering for the UDP zoom port. The payload is being saved as the length seen below, 8 bytes is being removed as that is the length of the UDP header. Below is an example of our code, this excerpt is from our UDP parsing.

```python
if (ip.p == dpkt.ip.IP_PROTO_UDP):
    #print(ip.p)
    # Grab data by port number 8801 = zoom
    if(pp.sport == 8801 or pp.dport == 8801):
        # Print out the timestamp in UTC
        time1 = datetime.datetime.utcfromtimestamp(timestamp)
        tt = time1.strftime('%H:%M:%S.%f')[:-4]
        # Finding interarrival time
        if (numPackets > 1):
            interArrival = (time1 - time2).total_seconds()
            timeArr.append(interArrival)
        # Payload size in bytes
        length = len(pp) - 8 #UDP header is 8 bytes
        lengthPackets.append(length)
        numPackets += 1
        time2 = datetime.datetime.utcfromtimestamp(timestamp)
```

After parsing out the data we saved them to CSV files so that we could use MatLab to generate the CDF and PDF of each sets of data.  

---

### How does the payload size distribution of different applications differ from each other?

### VoIP

Taking a look at VoIP, we see that the CDF of the interarrival time follows an exponential distribution . As time goes on, there is a higher probability that a packet will come in. The PDF also goes into line of the properties of VoIP. The protocol defines a certain amount of data to be sent for a period of time during a voice spurt. So it is expected that we see a large spike at 1032 which is most likely the datarate that zoom transmits its data.

| ![Image Caption](images/voippaycdf.PNG) | 
|----|
|![Image Caption](images/voippaypdf.PNG) |

### HTTP

For HTTP, we captured HTTP packets that were operating under the TCP protocol. As such, HTTP packets are only responsible for creating the data to be sent, since it is an application layer protocol. The actual packets are sent via TCP/UDP (TCP in this case). A large majority of the packets have a payload size of 1445, meaning that TCP split up the data to be sent in 1445 byte chunks as that is probably some max sized chunk it could send.  All of these 1460 sized payloads were labeled under info as 'continuation'.

| ![Image Caption](images/httppaycdf.PNG) |
|----|
| ![Image Caption](images/httppaypdf.PNG) |


<p float="left">
  <img src="images/httppaypdf.PNG" width="100" />
  <img src="images/httppaypdf.PNG" width="100" /> 
</p>

Solarized dark             |  Solarized Ocean
:-------------------------:|:-------------------------:
![](images/httppaypdf.PNG)  |  ![](images/httppaypdf.PNG)


### BitTorrent

For Bittorrent we are seeing a large concentration of payload sizes of 1514. It is using a TCP transport protocol so this may be the maximum chunk size or limit set by the client, or restricted by the maximum transmission unit.  Which would be the limit set by the hardware in the network. There's also a large concentration of 88 and 63 sized packets. We think these could be the messages being sent as acknowledgements and requests for chunks.  As the message type of the 63 sized payload is "Have" and the 88 is "Request". There's also a 451 sized chunk with the message "Unchoke" and a 242 sized payload with the message "Extended". This may be referring to the peer selection process, where it has evaluated a peer and chose to extend their connection or to unchoke a peer.

| ![Image Caption](images/bitpaycdf.PNG) |
|----|
| ![Image Caption](images/bitpaypdf.PNG) |

### FTP

The main messages in FTP are several small messages managing the navigation of the directories, or requesting a file or that a file has successfully be transferred.  When a file is being transferred it is done so over TCP. So FTP is solely many small varying messages.

| ![Image Caption](images/ftppaycdf.PNG) |
|----|
| ![Image Caption](images/ftppaypdf.PNG) |

---

### Explain your observations of the inter-arrival time distribution. 

The interarrival time of bitTorrent and VoIP both follow an exponential distribution. 

This may be due to the fact that these two protocols can be considered as poisson processes. For bitTorrent, the amount of packets that we receieve is ultimately dependent on tit=for-tat, meaning most of the time we have a fixed data rate. However, we do not necessarily know when we will be receiving packets, since bitTorrent also uses chunk selection algorithms, as well as the fact that we won't be downloading chunks we already have. This follows the general model of a poisson process.

For VoIP, we have a definitive data rate determined by Zoom, and since the voice spurts between two persons talking is random, this also fits a poisson process. As such, if we take the interarrival times of these poisson processes, we would receieve an exponential distribution (as discussed in ECE 158A)


---

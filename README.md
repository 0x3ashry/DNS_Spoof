# DNS_Spoof
It is a redirecting program that redirects the victum to your website instead of his visited website through DNS Spoofing after being MITM

## prerequisites:
You must have netfiterqueue library installed on your machine
  You can refer to: https://pypi.org/project/NetfilterQueue/

### Usage:
1. You must run first "sudo iptables -I FORWARD -j NFQUEUE --queue-num 0"
2. Edit the "www.bing.com" in line 13 with the website you are targeting
3. Edit the "website" pvariable in line 15 with the Ip address of your website
4. When you finish return the iptables to its original state "sudo iptables --flush"

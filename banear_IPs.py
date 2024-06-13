from scapy.all import rdpcap
import pandas as pd
import subprocess

""" 
ss -t -p
se recomienda usar el código de bash de arriba para ver cuáles procesos están usando puertos locales
"""
packets = rdpcap('dump-1718223419.pcap')   #tomar preferiblemente con nettsniff-ng (nethogs, tcpdump, tshark o el cortafuegos tambien pueden ayudar)
# ps -p <PID>          para ver el proceso especifico del .pcap en bash si se tiene el codigo PID

packet_data = []
for packet in packets:
    if packet.haslayer('IP'):
        packet_data.append({
            'Source IP': packet['IP'].src,
            'Destination IP': packet['IP'].dst,
            'Protocol': packet.sprintf("%IP.proto%"),
            'Length': len(packet)
        })

df = pd.DataFrame(packet_data)
df = df.sort_values(by='Source IP')
df = df[df['Source IP'] != '192.168.105.193'] #IP propia
unique_ips = df['Source IP'].unique()
print(df.head())

for ip_to_ban in unique_ips:
    try:
        subprocess.run(f"sudo iptables -A INPUT -s {ip_to_ban} -j DROP", shell=True, check=True)
        subprocess.run(f"sudo iptables -A OUTPUT -s {ip_to_ban} -j DROP", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"{e}")
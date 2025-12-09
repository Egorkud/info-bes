from scapy.all import sniff, ARP
from collections import defaultdict
import time

LOGFILE = "arp_events.log"
ip_to_macs = defaultdict(set)

def log(msg):
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"{ts} {msg}"
    print(line)
    with open(LOGFILE, "a") as f:
        f.write(line + "\n")

def handle(pkt):
    if not pkt.haslayer(ARP):
        return
    arp = pkt[ARP]
    src_ip = arp.psrc
    src_mac = arp.hwsrc

    macs = ip_to_macs[src_ip]

    if src_mac not in macs:
        macs.add(src_mac)
        if len(macs) == 1:
            log(f"INFO: New mapping {src_ip} -> {src_mac}")
        else:
            log(f"ALERT: {src_ip} now has multiple MACs: {list(macs)}")

print("[*] Starting ARP sniffer (analyzing ARP table changes)...")
sniff(filter="arp", prn=handle, store=False)


print("[*] Starting ARP sniffer (analyzing ARP table changes)...")
sniff(filter="arp", prn=handle, store=False)

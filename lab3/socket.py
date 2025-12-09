from scapy.all import srp, Ether, ARP, conf
import csv

NETWORK = "192.168.31.0/24"
OUTFILE = "devices.csv"

def scan(network_cidr, timeout=2):
    conf.verb = 0
    pkt = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=network_cidr)
    answered, _ = srp(pkt, timeout=timeout)
    devices = []
    for snd, rcv in answered:
        devices.append((rcv.psrc, rcv.hwsrc))
    return devices

def save_csv(devices, fname):
    with open(fname, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["ip", "mac"])
        for ip, mac in devices:
            w.writerow([ip, mac])
    print(f"[+] Saved {len(devices)} devices to {fname}")

print(f"[+] Scanning {NETWORK} ...")
devices = scan(NETWORK)
for ip, mac in devices:
    print(f"{ip:16} {mac}")
save_csv(devices, OUTFILE)

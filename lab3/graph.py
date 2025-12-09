import matplotlib.pyplot as plt
import networkx as nx
from scapy.all import ARP, Ether, srp, conf
from scapy.arch.windows import get_windows_if_list

# КРИТИЧНО для Windows
conf.checkIPaddr = False

target_network = "192.168.0.0/24"

# Автовиявлення Wi-Fi інтерфейсу
def find_npf_iface():
    for iface in get_windows_if_list():
        if iface["name"].startswith(r"\Device\NPF_"):
            # Тут можна додатково перевіряти "Wi-Fi" або "Ethernet" у description
            print(f"Using interface: {iface['name']} ({iface['description']})")
            return iface["name"]
    return None


iface_name = find_npf_iface()

# Сканування мережі
print(f"Сканую мережу {target_network} через інтерфейс '{iface_name}'...")

packet = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=target_network)
ans, _ = srp(packet, timeout=3, iface=iface_name, verbose=False)

devices = []
for sent, received in ans:
    devices.append({'ip': received.psrc, 'mac': received.hwsrc})

if not devices:
    print("Нічого не знайдено! Перевір інтерфейс і мережу.")
    exit()

# Вивід у консоль
print("\nЗнайдені пристрої:")
print("IP-адреса".ljust(18), "MAC-адреса")
print("-" * 50)
for d in devices:
    print(d['ip'].ljust(18), d['mac'])

# Побудова графа
G = nx.Graph()

for d in devices:
    G.add_node(d['ip'], type='IP')
    G.add_node(d['mac'], type='MAC')
    G.add_edge(d['ip'], d['mac'])

plt.figure(figsize=(14, 9))
pos = nx.spring_layout(G, k=1, iterations=50)

ip_nodes = [n for n, attr in G.nodes(data=True) if attr.get('type') == 'IP']
mac_nodes = [n for n, attr in G.nodes(data=True) if attr.get('type') == 'MAC']

nx.draw_networkx_nodes(G, pos, nodelist=ip_nodes, node_color='lightblue',
                       node_shape='s', node_size=3000, label='IP')
nx.draw_networkx_nodes(G, pos, nodelist=mac_nodes, node_color='lightcoral',
                       node_shape='o', node_size=2000, label='MAC')
nx.draw_networkx_edges(G, pos, width=2, alpha=0.6)
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

plt.legend(scatterpoints=1)
plt.title("ARP Table Visualization (IP ↔ MAC)", fontsize=16, pad=20)
plt.axis('off')
plt.tight_layout()
plt.savefig("arp_graph.png", dpi=200, bbox_inches='tight')
plt.show()

print("\nGraph saved as arp_graph.png")

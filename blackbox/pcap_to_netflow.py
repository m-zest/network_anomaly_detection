





from scapy.all import rdpcap, TCP, UDP, IP
import pandas as pd
from collections import defaultdict

# Load packets
packets = rdpcap("stealth_port_scan_80.pcap")

# Normalize flow keys: unordered 5-tuple (IP1, port1, IP2, port2, proto)
def get_flow_key(ip_src, ip_dst, sport, dport, proto):
    if (ip_src, sport) <= (ip_dst, dport):
        return (ip_src, sport, ip_dst, dport, proto)
    else:
        return (ip_dst, dport, ip_src, sport, proto)

# Flow stats container
flows = defaultdict(lambda: {
    'start': None,
    'end': None,
    'sbytes': 0,
    'spkts': 0,
    'proto': '',
    'flags': set()
})

# Parse packets
for pkt in packets:
    if IP in pkt and (TCP in pkt or UDP in pkt):
        proto = 'tcp' if TCP in pkt else 'udp'
        l4 = pkt[TCP] if TCP in pkt else pkt[UDP]
        ip = pkt[IP]

        sport = l4.sport
        dport = l4.dport
        proto_num = ip.proto
        pkt_time = float(pkt.time)
        pkt_len = len(pkt)

        flow_key = get_flow_key(ip.src, ip.dst, sport, dport, proto_num)

        flow = flows[flow_key]
        flow['start'] = pkt_time if flow['start'] is None else min(flow['start'], pkt_time)
        flow['end'] = pkt_time if flow['end'] is None else max(flow['end'], pkt_time)
        flow['sbytes'] += pkt_len
        flow['spkts'] += 1
        flow['proto'] = proto
        if TCP in pkt:
            flow['flags'].update(pkt[TCP].flags)

# Determine connection state
def classify_state(flags, spkts):
    flag_str = ''.join(str(f) for f in flags)
    if 'F' in flag_str:
        return 'FIN'
    elif 'S' in flag_str and 'A' in flag_str and spkts >= 3:
        return 'CON'
    else:
        return 'INT'

# Build DataFrame
rows = []
for key, data in flows.items():
    src, sport, dst, dport, proto = key
    dur = round(data['end'] - data['start'], 6)
    state = classify_state(data['flags'], data['spkts'])

    rows.append({
        'sport': sport,
        'dport': dport,
        'proto': proto,
        'state': state,
        'dur': dur,
        'sbytes': data['sbytes'],
        'spkts': data['spkts']
    })

df = pd.DataFrame(rows)
df.to_csv("stealth_port_scan_80.csv", index=False)
print("[*] Exported NetFlow-style CSV as 'netflow_output.csv'")





















'''

from scapy.all import rdpcap, TCP, UDP, IP
import pandas as pd
from collections import defaultdict

# Load packets
packets = rdpcap("port_scan_80.pcap")

# Structure: flow_key => [start_time, end_time, sbytes, spkts, proto, state]
flows = defaultdict(lambda: {
    'start': None,
    'end': None,
    'sbytes': 0,
    'spkts': 0,
    'proto': '',
    'flags': set()
})

for pkt in packets:
    if IP in pkt and (TCP in pkt or UDP in pkt):
        proto = 'tcp' if TCP in pkt else 'udp'
        l4 = pkt[TCP] if TCP in pkt else pkt[UDP]
        ip = pkt[IP]

        sport = l4.sport
        dport = l4.dport
        proto_num = ip.proto
        flow_key = (ip.src, ip.dst, sport, dport, proto_num)

        pkt_time = float(pkt.time)
        pkt_len = len(pkt)

        flow = flows[flow_key]
        flow['start'] = pkt_time if flow['start'] is None else min(flow['start'], pkt_time)
        flow['end'] = pkt_time if flow['end'] is None else max(flow['end'], pkt_time)
        flow['sbytes'] += pkt_len
        flow['spkts'] += 1
        flow['proto'] = proto
        if TCP in pkt:
            flow['flags'].add(pkt[TCP].flags)

# Convert to DataFrame
rows = []
for (src, dst, sport, dport, proto_num), data in flows.items():
    duration = data['end'] - data['start']
    state = ''
    if 'S' in ''.join(str(f) for f in data['flags']) and 'A' in ''.join(str(f) for f in data['flags']):
        state = 'ESTABLISHED'
    elif 'S' in ''.join(str(f) for f in data['flags']):
        state = 'SYN_SENT'
    elif 'R' in ''.join(str(f) for f in data['flags']):
        state = 'RESET'
    else:
        state = 'OTHER'

    rows.append({
        'sport': sport,
        'dport': dport,
        'proto': data['proto'],
        'state': state,
        'dur': round(duration, 6),
        'sbytes': data['sbytes'],
        'spkts': data['spkts']
    })

df = pd.DataFrame(rows)
df.to_csv("port_scan_80.csv", index=False)
print("[*] NetFlow-style CSV saved as 'netflow_output.csv'")
'''
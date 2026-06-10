import re

interfaces = []
current = None

switch = 'c3560g-L3Switch.conf'

with open(switch) as f:
    for line in f:
        clean = line.strip()
        if clean.startswith('interface'):
            current = {'name': clean.split()[1]}
            interfaces.append(current)
        elif clean.startswith('description'):
            current['description'] = ' '.join(clean.split()[1:])
        elif clean.startswith('ip address'):
            match = re.search(r'(\d+\.\d+\.\d+\.\d+)', clean)
            if match:
                current['IP address'] = match.group(1)

print(interfaces)
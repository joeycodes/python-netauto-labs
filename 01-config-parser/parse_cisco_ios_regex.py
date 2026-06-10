import re

switch = 'c3560g-L3Switch.conf'

with open (switch) as f:
    for line in f:
        clean = line.strip()
        if clean.startswith('interface'):
            print(clean.split()[1])
            match = re.search(r'(Vlan\d+)', clean)
            if match:
                print(match.group(1))
        elif clean.startswith('ip address'):
            match = re.search(r"(\d+\.\d+\.\d+\.\d+)", clean)
            if match:
                print(match.group(1))

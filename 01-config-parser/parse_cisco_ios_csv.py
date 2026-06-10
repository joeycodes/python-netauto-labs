import re
import csv

switch = 'c2911-router.conf'
csv_filename = 'interfaces.csv'

def interface_dict(config):
    
    interfaces = []
    current = None

    with open(config) as f:
        for line in f:
            clean = line.strip()
            if clean.startswith('interface'):
                current = {'name': clean.split()[1]}
                interfaces.append(current)
            elif clean.startswith('description') and current is not None:
                current['description'] = ' '.join(clean.split()[1:])
            elif clean.startswith('ip address') and current is not None:
                match = re.search(r'(\d+\.\d+\.\d+\.\d+)', clean)
                if match:
                    current['IP address'] = match.group(1)
    return interfaces

def interfaces_to_csv(filename, rows):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'description', 'IP address'])
        writer.writeheader()
        writer.writerows(rows)

if __name__ == "__main__":
    interfaces = interface_dict(switch)
    print(interfaces)
    interfaces_to_csv(csv_filename, interfaces)
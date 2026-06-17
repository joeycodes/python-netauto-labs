import yaml
import re
from datetime import date
import csv
import glob
import os

rule_file = 'rules/rules_defined.yml'
sample_config = 'config/c3560g-L3Switch.conf'
config_dir = 'config/'

def rules_reader(rules):
    with open(rules) as f:
        rules = yaml.safe_load(f)
    return rules

def intf_dict(config):
    
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
                    current['ip address'] = match.group(1)
            elif clean.startswith('shutdown'):
                current['state'] = 'down'
        for intf in interfaces:
            intf.setdefault('state', 'up')
    return interfaces

def read_config_lines(config):
    lines = []
    in_intf_block = False
    with open(config) as f:
        for line in f:
            clean = line.strip()
            if not clean or clean.startswith('!'):
                continue

            if not line.startswith(' '):
                in_intf_block = clean.startswith('interface')
                if not in_intf_block:
                    lines.append(clean)
            else:
                if not in_intf_block:
                    lines.append(clean)
    return lines

def get_hostname(global_lines):
    for line in global_lines:
        if line.startswith('hostname'):
            return line.split()[1]
    return 'unknown'

def intf_cond_met(interface, rule):
    expected = rule['condition']['state']
    return expected == interface.get('state')

## Check interface config to see if they meet the requirements listed on the rules.
def intf_checker(config, rules):
    violations = []
    interfaces = intf_dict(config)
    rules = rules_reader(rules)
    for interface in interfaces:
        for rule in rules['interface_rules']:        
            if 'condition' in rule and not intf_cond_met(interface, rule):
                continue
            actual_value = extract_interface(interface, rule)
            if run_check(actual_value, rule) is True:
                violations.append({'interface': interface['name'], 'rule': rule['name'], 'description': rule['description'], 'actual_value': actual_value})
    return violations

def extract_interface(interface, rule):
    return interface.get(rule['field'])

## Check global config to see if they meet the requirements listed on the rules.
def global_checker(config, rules):
    violations = []
    global_lines = read_config_lines(config)
    rules = rules_reader(rules)
    for rule in rules['global_rules']:
        actual_value = extract_global(global_lines, rule)
        if run_check(actual_value, rule) is True:
            violations.append({'rule': rule['name'], 'scope': 'device', 'description': rule['description'], 'actual_value': actual_value})
    return violations

def extract_global(global_lines, rule):
    for line in global_lines:
        if rule.get('match_line') in line:
            return line
    return None

# Separate function aside checkers for checking types.
def run_check(actual_value, rule):
    check = rule.get('check')
    if check == 'must_exist':
        return actual_value is None
    if check == 'must_not_contain':
        return actual_value is not None and rule.get('value') in actual_value
    elif check == 'must_match':
        return actual_value is None or not re.match(rule.get('value'), actual_value.split()[1])
    return False

def build_report(config, rules):
    global_lines = read_config_lines(config)
    hostname = get_hostname(global_lines)
    g_viol = global_checker(config, rules)
    i_viol = intf_checker(config, rules)

    rows = []

    for viol in g_viol:
        rows.append(to_row(hostname, viol.get('scope'), viol))

    for viol in i_viol:
        rows.append(to_row(hostname, viol.get('interface'), viol))

    return hostname, rows

def to_row(hostname, scope, viol):
    actual = viol.get('actual_value')
    actual = actual if actual is not None else "(Not configured)"
    return {
        'hostname': hostname,
        'scope': scope,
        'rule': viol.get('rule'),
        'description': viol.get('description'),
        'actual_value': actual
    }

def write_csv(filename, rows):
    fieldnames = ['hostname', 'scope', 'rule', 'description', 'actual_value']

    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return filename

def run_all(config_dir, rules):
    all_rows = []
    filenames = []
    today = date.today().strftime('%Y%m%d')
    config_files = glob.glob(os.path.join(config_dir, '*.conf'))
    for config in config_files:
        hostname, rows = build_report(config, rules)
        device_filename = f"{hostname}-compliance-{today}.csv"
        write_csv(device_filename, rows)
        all_rows.extend(rows)
        filenames.append(device_filename)
    
    aio_filename = f"all-device-compliance-{today}.csv"
    write_csv(aio_filename, all_rows)
    filenames.append(aio_filename)
    return filenames

if __name__ == "__main__":
    run_all(config_dir, rule_file)
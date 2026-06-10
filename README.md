# python-netauto-labs

A long-term, hands-on collection of Python labs for learning network automation.
Each lab is a self-contained project that builds practical skills — from parsing
device configs to interacting with live devices and orchestrating changes.

## Labs

| #  | Lab | What it does | Key skills |
|----|-----|--------------|------------|
| 01 | [config-parser](./01-config-parser) | Parses Cisco IOS configs and extracts per-interface data (name, description, IP) into CSV | file I/O, regex, dict/list modeling, csv |

## Why this repo

I want to use this repo to document and practice Python network automation — covering different areas from beginner to advanced, along with the relevant modules involved.

## Tech

- Python 3.x
- Standard library so far (`re`, `csv`); more tooling (Netmiko, Nornir, etc.) to come

## Note on sample data

All device configs in this repo are sample/lab. No real hostnames, IPs, or credentials. 

## Structure

​```
python-netauto-labs/
├── 01-config-parser/
│   ├── *parser.py
│   ├── csv-outputs
│   └── sample-configs
└── ...
​```
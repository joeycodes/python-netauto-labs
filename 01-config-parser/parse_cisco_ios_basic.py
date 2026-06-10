with open ('c2911-router.conf') as f:
    for line in f:
        clean = line.strip()
        if clean.startswith('interface'):
            print(clean.split()[1])
        elif clean.startswith('ip address'):
            print(clean.split()[2])
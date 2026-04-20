import csv

def load_findings(filename):
    with open(filename, newline='') as file:
        reader = csv.DictReader(file)
        return list(reader)

def count_by_field(findings, field):
    counts = {}
    for f in findings:
        key = f[field]
        counts[key] = counts.get(key, 0) + 1
    return counts

def filter_findings(findings, field, value):
    return [f for f in findings if f[field] == value]

def top_subdomains(findings, n):
    counts = {}
    for f in findings:
        sub = f["subdomain"]
        counts[sub] = counts.get(sub, 0) + 1

    sorted_list = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_list[:n]

class Finding:

    def __init__(self, subdomain, title, severity):
        self.subdomain = subdomain
        self.title = title
        self.severity = severity
        self.severity_rank = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}

    def __str__(self):
        return f"[{self.severity}] {self.subdomain} — {self.title}"

    def __eq__(self, other):
        return self.subdomain == other.subdomain and self.title == other.title

    def __lt__(self, other):
        return self.severity_rank[self.severity] < self.severity_rank[other.severity]


class Report:

    def __init__(self, team_name):
        self.team_name = team_name
        self.findings = []

    def add(self, finding):
        self.findings.append(finding)

    def __len__(self):
        return len(self.findings)

    def __add__(self, other):
        new_report = Report(f"Merged: {self.team_name} + {other.team_name}")
        new_report.findings = self.findings + other.findings
        return new_report


# --- Main ---
if __name__ == "__main__":
    print("=" * 60)
    print("  Q2: DUNDER METHODS")
    print("=" * 60)

    f1 = Finding("ssh.0x10.cloud", "Default creds", "HIGH")
    f2 = Finding("blog.0x10.cloud", "No HTTPS", "LOW")
    f3 = Finding("api.0x10.cloud", "Version exposed", "MEDIUM")
    f1_copy = Finding("ssh.0x10.cloud", "Default creds", "HIGH")

    print("\n--- Findings ---")
    print(f"  {f1}")
    print(f"  {f2}")
    print(f"  {f3}")

    print("\n--- Comparing ---")
    print(f"  f1 == f1_copy: {f1 == f1_copy}")
    print(f"  f1 == f2: {f1 == f2}")

    print("\n--- Sorting (LOW → HIGH) ---")
    findings = [f1, f2, f3]
    for f in sorted(findings):
        print(f"  {f}")

    print("\n--- Report Length ---")
    r1 = Report("Team Alpha")
    r1.add(f1)
    r1.add(f2)
    r2 = Report("Team Beta")
    r2.add(f3)

    print(f"  Team Alpha has {len(r1)} findings")
    print(f"  Team Beta has {len(r2)} findings")

    print("\n--- Merging Reports ---")
    merged = r1 + r2
    print(f"  {merged.team_name} has {len(merged)} findings")

    print("\n" + "=" * 60)

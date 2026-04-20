def bar_chart(data, title, max_width=30):
    print("\n", title)

    max_value = max(count for _, count in data)

    for label, count in data:
        bar_length = int((count / max_value) * max_width)
        bar = "█" * bar_length
        print(f"{label:<10} {bar} {count}")


def severity_summary(findings):
    counts = {"HIGH":0, "MEDIUM":0, "LOW":0}

    for f in findings:
        counts[f["severity"]] += 1

    return [("HIGH", counts["HIGH"]),
            ("MEDIUM", counts["MEDIUM"]),
            ("LOW", counts["LOW"])]


def timeline(findings):
    counts = {}

    for f in findings:
        date = f["date"]
        counts[date] = counts.get(date, 0) + 1

    return sorted(counts.items())

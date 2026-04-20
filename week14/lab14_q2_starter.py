import urllib.request

REQUIRED_HEADERS = {
    "Content-Type": "Defines the content format",
    "X-Frame-Options": "Vulnerable to clickjacking",
    "X-Content-Type-Options": "Vulnerable to MIME sniffing",
    "Strict-Transport-Security": "No HTTPS enforcement",
    "Content-Security-Policy": "No XSS protection policy",
    "X-XSS-Protection": "No XSS filter",
}

def check_headers(url):
    try:
        response = urllib.request.urlopen(url)
        headers = dict(response.headers)

        results = []

        for header in REQUIRED_HEADERS:
            if header in headers:
                results.append({
                    "header": header,
                    "present": True,
                    "value": headers[header]
                })
            else:
                results.append({
                    "header": header,
                    "present": False,
                    "value": "MISSING"
                })

        return results

    except Exception:
        return []

def generate_report(url, results):
    print(url)
    missing = 0

    for r in results:
        if r["present"]:
            print(f"✓ {r['header']}: {r['value']}")
        else:
            print(f"✗ {r['header']}: MISSING — {REQUIRED_HEADERS[r['header']]}")
            missing += 1

    print(f"Missing {missing} of {len(results)} headers")


if __name__ == "__main__":
    urls = [
        "http://httpbin.org",
        "https://www.google.com"
    ]

    for url in urls:
        print("\nChecking:", url)
        results = check_headers(url)
        generate_report(url, results)

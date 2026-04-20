import urllib.request
import json

def make_request(url):
    try:
        response = urllib.request.urlopen(url)
        body = response.read().decode()
        return {
            "status": response.status,
            "headers": dict(response.headers),
            "body": body
        }
    except Exception as e:
        return {
            "status": 0,
            "headers": {},
            "body": "",
            "error": str(e)
        }

def parse_json(body):
    try:
        return json.loads(body)
    except Exception:
        return None

def check_api_info(response):
    findings = []
    headers = response.get("headers", {})

    if "Server" in headers:
        findings.append(f"Server version exposed: {headers['Server']}")

    if "X-Powered-By" in headers:
        findings.append(f"Technology exposed: {headers['X-Powered-By']}")

    if headers.get("Access-Control-Allow-Origin") == "*":
        findings.append("CORS: open to all origins")

    return findings


if __name__ == "__main__":
    url = "http://httpbin.org/headers"
    resp = make_request(url)

    if resp and resp.get("status"):
        print("Status:", resp["status"])
        print("\nHeaders:")
        for k, v in resp["headers"].items():
            print(k, ":", v)

        print("\nJSON:")
        data = parse_json(resp["body"])
        print(data)

        print("\nFindings:")
        for f in check_api_info(resp):
            print(f)

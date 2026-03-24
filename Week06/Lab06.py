# ============================================================
#  WEEK 06 LAB: NETWORK DIAGNOSTIC LOGGER
#  COMP2152
#  Asal Ghafoory
# ============================================================

import subprocess
import csv
from datetime import datetime


# ============================================================
#  SECTION A: Running System Commands
# ============================================================

def run_ping(host):
    result = subprocess.run(
        ["ping", "-c", "3", host],
        capture_output=True, text=True
    )
    return result.stdout


def run_nslookup(domain):
    result = subprocess.run(
        ["nslookup", domain],
        capture_output=True, text=True
    )
    return result.stdout


def get_network_info():
    result = subprocess.run(
        ["ifconfig", "en0"],
        capture_output=True, text=True
    )
    return result.stdout


def get_arp_table():
    result = subprocess.run(
        ["arp", "-a"],
        capture_output=True, text=True
    )
    return result.stdout


def get_hostname():
    result = subprocess.run(
        ["hostname"],
        capture_output=True, text=True
    )
    return result.stdout.strip()


# ============================================================
#  SECTION B: Parsing Command Output
# ============================================================

def parse_ping(output):
    lines = output.strip().split("\n")
    stats = {
        "transmitted": 0,
        "received": 0,
        "loss": "100%",
        "avg_ms": "N/A",
        "status": "Failed"
    }

    for line in lines:
        if "packets transmitted" in line:
            parts = line.split(", ")
            stats["transmitted"] = int(parts[0].split()[0])
            stats["received"] = int(parts[1].split()[0])
            stats["loss"] = parts[2].split()[0]

        if "round-trip" in line or "rtt" in line:
            times = line.split("=")[1].strip().split("/")
            stats["avg_ms"] = times[1]

    if stats["received"] > 0:
        stats["status"] = "Success"

    return stats


def parse_nslookup(output):
    lines = output.strip().split("\n")
    result = {"ip": "Not found", "status": "Failed"}

    found_answer = False
    for line in lines:
        if "Non-authoritative answer" in line:
            found_answer = True
        if found_answer and "Address:" in line:
            ip = line.split("Address:")[1].strip()
            if "." in ip:
                result["ip"] = ip
                result["status"] = "Success"
                break

    return result


def parse_mac_address(output):
    lines = output.strip().split("\n")
    info = {"mac": "Not found", "ip": "Not found"}

    for line in lines:
        line = line.strip()
        if line.startswith("ether"):
            info["mac"] = line.split()[1]
        if "inet " in line and "inet6" not in line:
            info["ip"] = line.split()[1]

    return info


def parse_arp_table(output):
    lines = output.strip().split("\n")
    devices = []

    for line in lines:
        if "at" in line and "on" in line:
            parts = line.split()
            ip = "unknown"
            mac = "unknown"

            for part in parts:
                if part.startswith("(") and part.endswith(")"):
                    ip = part[1:-1]

            at_index = parts.index("at")
            if at_index + 1 < len(parts):
                mac = parts[at_index + 1]

            devices.append({"ip": ip, "mac": mac})

    return devices


# ============================================================
#  SECTION C: File I/O — Text Files
# ============================================================

def write_to_log(filename, entry):
    with open(filename, "a") as file:
        file.write(entry + "\n")


def read_log(filename):
    with open(filename, "r") as file:
        return file.read()


def log_command_result(command_name, target, output, filename):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = "[" + timestamp + "] " + command_name + " " + target + "\n"
    entry += output
    entry += "-" * 40
    write_to_log(filename, entry)


# ============================================================
#  SECTION D: File I/O — CSV Files
# ============================================================

LOG_FILE = "diagnostics.csv"


def log_to_csv(filename, command, target, result, status):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, command, target, result, status])


def read_csv_log(filename):
    with open(filename, "r", newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            print(" | ".join(row))


def analyze_csv_log(filename):
    with open(filename, "r", newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)

    if len(rows) == 0:
        print("Log is empty.")
        return

    print("Total entries:", len(rows))

    command_counts = {}
    status_counts = {}

    for row in rows:
        command = row[1]
        status = row[4]

        command_counts[command] = command_counts.get(command, 0) + 1
        status_counts[status] = status_counts.get(status, 0) + 1

    print("\nCommands run:")
    for cmd in command_counts:
        print(" ", cmd, ":", command_counts[cmd])

    print("\nResults:")
    for status in status_counts:
        print(" ", status, ":", status_counts[status])


# ============================================================
#  SECTION E: Exception Handling
# ============================================================

def safe_ping(host):
    try:
        result = subprocess.run(
            ["ping", "-c", "3", host],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout if result.returncode == 0 else "Ping failed."
    except subprocess.TimeoutExpired:
        return "Ping timed out."
    except Exception as e:
        return str(e)


def safe_nslookup(domain):
    try:
        result = subprocess.run(
            ["nslookup", domain],
            capture_output=True, text=True, timeout=10
        )
        return parse_nslookup(result.stdout)
    except:
        return {"ip": "Error", "status": "Failed"}


def safe_read_log(filename):
    try:
        with open(filename, "r") as file:
            content = file.read()
            if content == "":
                print("Log file is empty.")
                return ""
            return content
    except FileNotFoundError:
        print("No log file found. Run a diagnostic first.")
        return ""
    finally:
        print("Log read attempt completed.")


# ============================================================
#  MAIN PROGRAM
# ============================================================

def main():
    print("Network Diagnostic Logger")

    while True:
        print("\n1. Ping")
        print("2. DNS Lookup")
        print("3. Exit")

        choice = input("Choose: ")

        if choice == "1":
            host = input("Enter host: ")
            output = safe_ping(host)
            print(output)
            log_to_csv(LOG_FILE, "ping", host, "done", "Success")

        elif choice == "2":
            domain = input("Enter domain: ")
            result = safe_nslookup(domain)
            print(result)
            log_to_csv(LOG_FILE, "nslookup", domain, result["ip"], result["status"])

        elif choice == "3":
            break


# RUN PROGRAM
main()
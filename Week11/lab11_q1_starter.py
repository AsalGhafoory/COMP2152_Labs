import socket

class SimpleScanner:

    def __init__(self, target):
        self.target = target
        self.open_ports = []

    def scan_port(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        try:
            result = sock.connect_ex((self.target, port))
            if result == 0:
                print(f"  Port {port}: OPEN")
                self.open_ports.append(port)
                return True
            return False
        finally:
            sock.close()

    def scan_range(self, start_port, end_port):
        for port in range(start_port, end_port + 1):
            self.scan_port(port)

    def display_results(self):
        print(f"  Results for {self.target}:")
        if not self.open_ports:
            print("    No open ports found.")
        else:
            for port in self.open_ports:
                print(f"    Port {port}")
import urllib.request
from html.parser import HTMLParser
import socket
import threading
import os
import sys
from datetime import datetime
from blacknet_os.utils import clear, save_to_log

# === BlackWebEngineView ===
class HackerHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output = []
        self.links = []
        self.in_title = self.in_p = self.in_a = False
        self.current_link = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'title': self.in_title = True
        elif tag == 'p': self.in_p = True
        elif tag == 'a':
            self.in_a = True
            for attr in attrs:
                if attr[0] == 'href':
                    self.current_link = attr[1]

    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
        elif tag == 'p': self.in_p = False
        elif tag == 'a':
            self.in_a = False
            self.current_link = ""

    def handle_data(self, data):
        if self.in_title:
            self.output.append(f"\n[TITLE] {data}\n")
        elif self.in_p:
            self.output.append(f"{data}\n")
        elif self.in_a:
            self.links.append((data.strip(), self.current_link))
            self.output.append(f"[{len(self.links)}] {data.strip()} ")

def BlackWebEngineView(url=None):
    if not url:
        url = input("Enter URL to browse: ")
    if not url.startswith("http"):
        url = "http://" + url
    try:
        html = urllib.request.urlopen(url).read().decode("utf-8", errors="ignore")
        parser = HackerHTMLParser()
        parser.feed(html)
        clear()
        print("".join(parser.output))
        if parser.links:
            print("\nAvailable Links:")
            for i, (text, link) in enumerate(parser.links):
                print(f"[{i + 1}] {text} -> {link}")
            choice = input("Choose a link #: ")
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(parser.links):
                    BlackWebEngineView(parser.links[idx][1])
    except Exception as e:
        print(f"Error: {e}")

# === BlackPortScanner ===
def BlackPortScanner():
    target = input("Target IP: ")
    ports = [21, 22, 23, 25, 53, 80, 110, 443, 8080]
    print(f"\n[!] Scanning {target}...")

    def scan_port(p):
        try:
            s = socket.socket()
            s.settimeout(0.5)
            s.connect((target, p))
            print(f"[+] Port {p} open")
            s.close()
        except:
            pass

    threads = []
    for port in ports:
        t = threading.Thread(target=scan_port, args=(port,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

# === BlackBackDoor ===
def BlackBackDoor():
    host = input("Listen on IP: ")
    port = int(input("Port: "))
    s = socket.socket()
    s.bind((host, port))
    s.listen(1)
    print(f"[+] Waiting for connection on {host}:{port}...")
    conn, addr = s.accept()
    print(f"[+] Connected: {addr}")
    while True:
        cmd = input("shell> ")
        if cmd.strip() == "exit":
            break
        conn.send(cmd.encode())
        print(conn.recv(4096).decode())
    conn.close()

# === BlackKeyLog ===
def BlackKeyLog():
    print("Starting keylogger - press Ctrl+C to stop")
    try:
        while True:
            key = sys.stdin.read(1)
            save_to_log(f"KEY: {key}")
    except KeyboardInterrupt:
        print("\n[!] Keylogger stopped")

# === BlackLanSweep ===
def BlackLanSweep():
    print("Sweeping local subnet...")
    base = input("Base IP (e.g., 192.168.1): ")
    for i in range(1, 255):
        ip = f"{base}.{i}"
        try:
            socket.gethostbyaddr(ip)
            print(f"[+] Active Host: {ip}")
        except:
            pass

# === BlackExec ===
def BlackExec():
    print("Entering evil Python exec mode. Type 'exit' to leave.")
    while True:
        code = input(">>> ")
        if code.lower() == 'exit':
            break
        try:
            exec(code)
        except Exception as e:
            print(f"Error: {e}")

# === Debugging Helper ===
def test_load_url():
    # Checking if 'load_url' or a similar function is initialized before calling it.
    # Replace with actual 'load_url' logic if needed.
    url_loader = None  # Simulating the URL loader initialization, which should be properly set
    
    if url_loader is None:
        print("Error: URL loader not initialized!")
    else:
        try:
            url_loader.load_url("http://example.com")
        except AttributeError as e:
            print(f"Error: {e}")

# Example call to test URL loading
test_load_url()


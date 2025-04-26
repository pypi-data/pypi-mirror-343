import os
import sys
from datetime import datetime

# === Terminal Colors ===
GREEN = '\033[92m'
RED = '\033[91m'
CYAN = '\033[96m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def save_to_log(data, filename="blacknet_log.txt"):
    with open(filename, 'a') as f:
        f.write(f"[{datetime.now()}] {data}\n")

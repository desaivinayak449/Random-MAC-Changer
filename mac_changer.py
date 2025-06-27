import subprocess
import re
import random

def get_random_mac():
    mac = [ 0x00, 0x16, 0x3e,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff) ]
    return ':'.join(map(lambda x: "%02x" % x, mac))

def change_mac(interface, new_mac):
    try:
        subprocess.run(["sudo", "ifconfig", interface, "down"], check=True)
        subprocess.run(["sudo", "ifconfig", interface, "hw", "ether", new_mac], check=True)
        subprocess.run(["sudo", "ifconfig", interface, "up"], check=True)
        print(f"[+] MAC address for {interface} changed to {new_mac}")
    except subprocess.CalledProcessError:
        print("[-] Failed to change MAC address. Are you root and is the interface correct?")

def get_current_mac(interface):
    result = subprocess.run(["ifconfig", interface], capture_output=True, text=True)
    mac_match = re.search(r"ether ([0-9a-f:]{17})", result.stdout)
    if mac_match:
        return mac_match.group(1)
    return None

# Usage
interface = "wlp0s20f3"  # or "wlan0", etc. Adjust to your system
current_mac = get_current_mac(interface)
print(f"[*] Current MAC: {current_mac}")

new_mac = get_random_mac()
change_mac(interface, new_mac)

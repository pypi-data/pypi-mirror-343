import socket
import ipaddress
import subprocess

class IP:
    def __init__(self, ip):
        self.ip = ip
        self.ip_obj = ipaddress.ip_address(ip)
    
    def is_private(self):
        return self.ip_obj.is_private
    
    def to_binary(self):
        return bin(int(self.ip_obj))[2:]
    
    def to_integer(self):
        return int(self.ip_obj)
    
    def is_in_network(self, network):
        net = ipaddress.IPv4Network(network)
        return self.ip_obj in net

def cidr_to_ip_range(cidr):
    network = ipaddress.IPv4Network(cidr, strict=False)
    return network.network_address, network.broadcast_address

def classify_ip(ip):
    ip_obj = ipaddress.ip_address(ip)
    if ip_obj.is_private:
        return 'Private'
    elif ip_obj.is_loopback:
        return 'Loopback'
    else:
        return 'Public'

def validate_ip_in_network(ip, network_range):
    network = ipaddress.IPv4Network(network_range)
    return ipaddress.ip_address(ip) in network

def reverse_dns_lookup(ip):
    try:
        return socket.gethostbyaddr(ip)
    except socket.herror:
        return None

def ip_to_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)
    except socket.herror:
        return None

def binary_to_ip(binary):
    return str(ipaddress.ip_address(int(binary, 2)))

def integer_to_ip(integer):
    return str(ipaddress.ip_address(integer))

def ip_to_binary(ip):
    return bin(int(ipaddress.ip_address(ip)))[2:]

def ip_to_integer(ip):
    return int(ipaddress.ip_address(ip))

def ping_ip(ip):
    try:
        response = subprocess.run(
            ["ping", "-n", "1", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return response.returncode == 0
    except FileNotFoundError:
        return False

def mask_ip(ip):
    parts = ip.split('.')
    parts[2] = '*'
    parts[3] = '*'
    return '.'.join(parts)

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
    except ValueError:
        raise ValueError(f"{ip} is not a valid IP address")

def validate_ip_batch(ips):
    return {ip: validate_ip(ip) for ip in ips}

# Special Easter Egg function :3
def special_3():
    print(":3")

# Example Usage
if __name__ == "__main__":
    # Validation Results
    ips = ["192.168.1.1", "8.8.8.8", "2606:2800:220:1:248:1893:25c8:1946"]
    for ip in ips:
        print(f"{ip} is {classify_ip(ip)}")
    
    # IP to Binary and Integer Conversion
    print("\nIP to Binary and Integer Conversion:")
    for ip in ips:
        print(f"{ip} in binary: {ip_to_binary(ip)}")
        print(f"{ip} in integer: {ip_to_integer(ip)}")
    
    # Private IP Check
    print("\nPrivate IP Check:")
    for ip in ips:
        print(f"{ip} is private? {IP(ip).is_private()}")
    
    # Network Info for IPs
    print("\nNetwork Info for IPs:")
    for ip in ips:
        network_info = None
        if classify_ip(ip) == "Private":
            network_info = {'network': ipaddress.IPv4Network(f'{ip}/24', strict=False).network_address, 'host': ip}
        print(f"{ip} Network Info: {network_info}")

    # CIDR to IP Range
    print("\nCIDR to IP Range Conversion:")
    print(f"192.168.1.0/24 -> Network Range: {cidr_to_ip_range('192.168.1.0/24')}")

    # Ping a Host
    print("\nPing Test:")
    print(f"Ping 8.8.8.8: {ping_ip('8.8.8.8')}")

    # Reverse DNS Lookup
    print("\nReverse DNS Lookup:")
    print(f"Reverse DNS for 8.8.8.8: {reverse_dns_lookup('8.8.8.8')}")

    # Mask IP
    print("\nMask IP:")
    print(f"Masking 192.168.1.1: {mask_ip('192.168.1.1')}")

    # Batch IP Validation
    print("\nBatch IP Validation:")
    ips_to_validate = ["192.168.1.1", "8.8.8.8", "invalid_ip"]
    print(validate_ip_batch(ips_to_validate))

# Special Easter Egg colon 3
def colon_3():
    expressions = [";3", "xD", ";P", ";3"]
    for expression in expressions:
        print(expression)

# Call the function
colon_3()

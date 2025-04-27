# KryoIP

KryoIP is a Python library designed to simplify the handling and manipulation of IP addresses. Whether you're working with IPv4 or IPv6 addresses, KryoIP provides a set of utility functions for validation, conversion, network checks, and more.

## Installation

You can install KryoIP using pip:

```bash
pip install kryoip

Features

KryoIP includes a variety of functions to help you work with IP addresses:

    IP Validation: Check if an IP address is valid and whether it's private or public.

    IP Conversion: Convert IP addresses to binary and integer formats.

    CIDR Operations: Convert CIDR blocks to IP ranges.

    Ping Test: Perform a basic ping test to check if an IP address is reachable.

    Reverse DNS Lookup: Perform a reverse DNS lookup to find the hostname for an IP address.

    Network Info: Get network information for an IP address, including its network and host address.

    IP Masking: Mask part of an IP address for privacy.

    Special Easter Egg: A fun little Easter egg that prints :3.

Functions
1. class IP

A class to manage and manipulate IP addresses.
Methods:

    is_private(): Checks if the IP is private.

    to_binary(): Converts the IP to binary format.

    to_integer(): Converts the IP to integer format.

    is_in_network(network): Checks if the IP is within a given network.

2. cidr_to_ip_range(cidr)

Converts a CIDR block to a range of IPs.

cidr_to_ip_range('192.168.1.0/24')  # Returns ('192.168.1.0', '192.168.1.255')

3. classify_ip(ip)

Classifies the IP address as 'Private', 'Loopback', or 'Public'.

classify_ip('192.168.1.1')  # Returns 'Private'

4. validate_ip_in_network(ip, network_range)

Validates if an IP address is within a given network range.

validate_ip_in_network('192.168.1.1', '192.168.1.0/24')  # Returns True

5. reverse_dns_lookup(ip)

Performs a reverse DNS lookup to find the hostname for an IP address.

reverse_dns_lookup('8.8.8.8')  # Returns ('dns.google', ['8.8.8.8'])

6. ping_ip(ip)

Pings an IP address to check if it's reachable.

ping_ip('8.8.8.8')  # Returns True if the host is reachable

7. mask_ip(ip)

Masks the IP address by replacing the last two octets with *.

mask_ip('192.168.1.1')  # Returns '192.168.*.*'

8. validate_ip(ip)

Validates if an IP address is correctly formatted.

validate_ip('192.168.1.1')  # Returns None if valid, raises ValueError if invalid

9. validate_ip_batch(ips)

Validates a batch of IPs and returns a dictionary of results.

validate_ip_batch(['192.168.1.1', '8.8.8.8', 'invalid_ip'])
# Returns: {'192.168.1.1': None, '8.8.8.8': None, 'invalid_ip': ValueError('invalid_ip is not a valid IP address')}

10. Special Easter Egg

special_3()  # Prints ':3'

Example Usage

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

Contributing

If you'd like to contribute to KryoIP, feel free to open an issue or submit a pull request. All contributions are welcome!
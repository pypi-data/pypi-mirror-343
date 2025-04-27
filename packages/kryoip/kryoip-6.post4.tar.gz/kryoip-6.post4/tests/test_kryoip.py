import kryoip

# Test with a known reachable IP address
reachable_ip = "8.8.8.8"
result_reachable = kryoip.ping_ip(reachable_ip)
print(f"Ping to {reachable_ip}: {result_reachable}")

# Test with a potentially unreachable IP address (you might need to adjust this)
unreachable_ip = "192.168.1.200"
result_unreachable = kryoip.ping_ip(unreachable_ip)
print(f"Ping to {unreachable_ip}: {result_unreachable}")

# Test with an invalid IP address format
invalid_ip = "not an ip"
result_invalid = kryoip.ping_ip(invalid_ip)
print(f"Ping to '{invalid_ip}': {result_invalid}")
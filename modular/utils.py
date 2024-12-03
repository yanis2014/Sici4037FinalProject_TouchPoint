def validate_ip(ip):
    try:
        parts = ip.split('.')
        if not (len(parts) == 4 and all(0 <= int(part) <= 255 for part in parts)):
            return f"Invalid IP Address: '{ip}'"
        return ""
    except ValueError:
        return f"Invalid IP Address: '{ip}'"

def validate_port(port):
    try:
        if not (0 <= int(port) <= 65535):
            return f"Invalid Port: '{port}'"
        return ""
    except ValueError:
        return f"Invalid Port: '{port}'"
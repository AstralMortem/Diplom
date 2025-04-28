import socket
import platform

from zeroconf import ServiceInfo, Zeroconf

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"
    
def register_mdns_service(port):
    local_ip = get_local_ip()
    hostname = platform.node()

    zeroconf = Zeroconf()

    service_info = ServiceInfo(
        "_myapp._tcp.local.",
        f"MyAppBackend._myapp._tcp.local.",
        addresses=[socket.inet_aton(local_ip)],
        port=port,
        properties={
            'version': '1.0.0',
            'serverName': hostname,
            'server_type': 'fastapi'
        }
    )
    zeroconf.register_service(service_info)
    return zeroconf, service_info
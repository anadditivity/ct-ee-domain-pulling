## The following is a simple POC.
import socket, ssl, OpenSSL
from urllib.parse import urlparse

def get_cert(domain):
    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=domain,
    )
    conn.connect((domain, 443))
    cert = conn.getpeercert(True)
    return cert

domains = ['example.com', 'neti.ee', 'facebook.com']
for domain in domains:
    with open(f'certificates/{domain}.pem', 'wb') as f:
        f.write(get_cert(domain))

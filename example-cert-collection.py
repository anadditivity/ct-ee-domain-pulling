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

domains = ['example.com', 'neti.ee',
           # my domain that doesn't have a server nor an SSL cert
           'anadditivity.eu',
           # website that instantly redirects to another site
           'sugu.ee',
           'facebook.com']
counter = 0
for domain in domains:
    try:
        cert = get_cert(domain)
        with open(f'certificates/{domain}.pem', 'wb') as f:
            f.write(cert)
        counter += 1
    except ssl.SSLError:
        continue

print(f'Out of {len(domains)}, managed to get {counter} certificates')

## The following is created with help from Mistral's Le Chat (troubleshooting and error logging)
import socket, ssl, time, os
from urllib.parse import urlparse

os.makedirs('certificates', exist_ok=True)

downloaded = set()
for f in os.listdir('certificates'):
    if f.endswith('.pem'):
        domain = f.replace('.pem', '')
        downloaded.add(domain)
print(f'Found {len(downloaded)} already downloaded certificates.')

def get_cert(domain):
    context = ssl.create_default_context()
    conn = None
    try:
        conn = context.wrap_socket(
            socket.socket(socket.AF_INET),
            server_hostname=domain,
        )
        conn.settimeout(10)
        conn.connect((domain, 443))
        cert = conn.getpeercert(True)
        return cert
    except socket.gaierror:
        print(f'DNS resolution failed for {domain}')
        return None
    except ssl.SSLError as e:
        print(f'SSL error for {domain}: {e}')
        return None
    except socket.timeout:
        print(f'Connection timeout for {domain}')
        return None
    except Exception as e:
        print(f'Unexpected error for {domain}: {e}')
        return None
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

domains = []
with open('neti-link-scrape-regex-cleaned.csv', 'r') as f:
    domains = f.read().strip().split('\n')

print(f'Loaded {len(domains)} domains to check.')

counter = 0
new_counter = 0
for domain in domains:
    if domain in downloaded:
        print(f'Skipping {domain} (already downloaded)')
        continue
    try:
        print(f'Checking {domain}...')
        cert = get_cert(domain)
        if cert:
            with open(f'certificates/{domain}.pem', 'wb') as f:
                f.write(cert)
            new_counter += 1
            print(f'Success: {domain} ({new_counter} new)')
            time.sleep(1)  # Be polite
    except KeyboardInterrupt:
        print('\nScript interrupted by user.')
        break
    except Exception as e:
        print(f'Error processing {domain}: {e}')

print(f'Out of {len(domains)}, {len(downloaded)} already downloaded, fetched {new_counter} new certificates')

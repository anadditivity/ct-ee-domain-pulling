## The following is created with help from Mistral's Le Chat (troubleshooting and error logging)
import socket, ssl, time, os
from urllib.parse import urlparse

os.makedirs('certificates', exist_ok=True)
os.makedirs('eu-certificates', exist_ok=True)
downloaded = set()
for f in os.listdir('certificates'):
    if f.endswith('.der'):
        domain = f.replace('.der', '')
        downloaded.add(domain)
for f in os.listdir('eu-certificates'):
    if f.endswith('.der'):
        domain = f.replace('.der', '')
        downloaded.add(domain)
print(f'Found {len(downloaded)} already downloaded certificates.')

def log_error(domain, error_type, error_message):
    with open('domain-collection/errored-domains/errored-eu-domains.txt', 'a') as f:
        f.write(f'{domain},{error_type},{error_message}\n')

def get_cert(domain):
    context = ssl.create_default_context()
    conn = None
    try:
        conn = context.wrap_socket(
            socket.socket(socket.AF_INET),
            server_hostname=domain,
        )
        conn.settimeout(1)
        conn.connect((domain, 443))
        cert = conn.getpeercert(True)
        return cert
    except socket.gaierror as e:
        print(f'DNS resolution failed for {domain}')
        log_error(domain, 'DNS resolution failed', str(e))
        return None
    except ssl.SSLError as e:
        print(f'SSL error for {domain}: {e}')
        log_error(domain, 'SSL error', str(e))
        return None
    except socket.timeout as e:
        print(f'Connection timeout for {domain}')
        log_error(domain, 'Connection timeout', str(e))
        return None
    except Exception as e:
        print(f'Unexpected error for {domain}: {e}')
        log_error(domain, 'Unexpected error', str(e))
        return None
    finally:
        if conn:
            try:
                conn.close()
            except:
                pass

domains = []
with open('domain-collection/found-domains/unique_eu_domains.csv', 'r') as f:
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
            with open(f'eu-certificates/{domain}.der', 'wb') as f:
                f.write(cert)
            new_counter += 1
            print(f'Success: {domain} ({new_counter} new)')
            time.sleep(0.1)  # I will be a little less polite for the EU domains ):
    except KeyboardInterrupt:
        print('\nScript interrupted by user.')
        break
    except Exception as e:
        print(f'Error processing {domain}: {e}')
        log_error(domain, 'Unexpected error in main loop', str(e))

print(f'Out of {len(domains)}, {len(downloaded)} already downloaded, fetched {new_counter} new certificates')

import re
import nmap
import subprocess
import os

def find_tls(url):
    nmap_command = 'nmap --script ssl-enum-ciphers -p 443 ' + url
    output = subprocess.getoutput(nmap_command)
    tls_versions = ['TLSv1.0', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3']
    real_tls_version = []

    for version in tls_versions:
        real_tls_version += re.findall(version, output)

    real_tls_version = list(filter(None, real_tls_version))
    print(url," ondersteunt  de volgende TLS-versies:", ', '.join(real_tls_version))
    
# find_tls('howsmyssl.com')
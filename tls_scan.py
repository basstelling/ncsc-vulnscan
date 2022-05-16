import re
import subprocess

def find_tls(url):
    if "https://www." in url:
        url = url[12:]
    nmap_command = 'nmap --script ssl-enum-ciphers -p 443 ' + url
    output = subprocess.getoutput(nmap_command)
    # print(output)
    tls_versions = ['TLSv1.0', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3']
    warning = False
    real_tls_version = []

    for version in tls_versions:
        real_tls_version += re.findall(version, output)

    real_tls_version = list(filter(None, real_tls_version))
    print("[i]", url," ondersteunt  de volgende TLS-versies:", ', '.join(real_tls_version))
    if ("TLSv1.0" in real_tls_version) or ("TLSv1.1" in real_tls_version):
        print("[!] LET OP:", url, "ondersteunt versie(s) van TLS onder TLSv1.2!")
    
# demo
# find_tls('nu.nl')
# find_tls('vpn.phoenixus.com')
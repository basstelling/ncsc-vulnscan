import re
import subprocess
from ncsc_config import read_config

def find_tls(url):
    if "https://www." in url:
        url = url[12:]
    nmap_command = 'nmap --script ssl-enum-ciphers -p 443 ' + url
    output = subprocess.getoutput(nmap_command)
    output_lines = output.splitlines()

    good_tls_ciphers = read_config('Cipher Suites', 'Goed').split('\n')
    ok_tls_ciphers = read_config('Cipher Suites', 'Voldoende').split('\n')
    bad_tls_ciphers = read_config('Cipher Suites', 'Uit te faseren').split('\n')
    tls_versions = read_config('TLS', 'versie').split('\n')

    used_ciphers = {"Goed":[], "Voldoende":[], "Uit te faseren":[]}
    used_tls_versions = []

    for line in output_lines:
        for cipher in good_tls_ciphers:
            if cipher in line:
                if "Goed" in used_ciphers:
                    used_ciphers['Goed'].append(str(cipher))
                else:
                    used_ciphers['Goed'] += cipher
        for cipher in ok_tls_ciphers:
            if cipher in line:
                if "Voldoende" in used_ciphers:
                    used_ciphers['Voldoende'].append(str(cipher))
                else:
                    used_ciphers['Voldoende'] += [cipher]
        for cipher in bad_tls_ciphers:
            if cipher in line:
                if 'Uit te faseren' in used_ciphers:
                    used_ciphers['Uit te faseren'].append(str(cipher))
                else:
                    used_ciphers['Voldoende'] += [cipher]
        for tls in tls_versions:
            if tls in line:
                used_tls_versions.append(tls)

    print("[i]",url,"maakt gebruik van TLS-versies:", ', '.join(used_tls_versions))

    for classificatie, cipher in used_ciphers.items():
        print("[i] Classificatie:", classificatie)
        print("[i]", len(cipher), "ciphers gevonden. ")
        for c in cipher:
            print("[*]", c)
    
# demo
# find_tls('nu.nl')
# find_tls('vpn.phoenixus.com')
# find_tls('martiniziekenhuis.nl')
import re
import subprocess
from src.ncsc_config import read_config

def find_tls(url):
    if "https://www." in url:
        url = url[12:]
    elif "http://www." in url:
        url = url[11:]
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
    length = sum([1 if isinstance(used_ciphers[a], (str, int))
            else len(used_ciphers[a])
            for a in used_ciphers])
    print(f"[i] {url} maakt gebruik van {length} ciphers.")

    for classificatie, cipher in used_ciphers.items():
        if len(cipher) != 0:
            # print("[i] Classificatie:", classificatie)
            # print(f"[i] Voor NCSC-classificatie {classificatie.lower()} zijn {len(cipher)} ciphers gevonden")
            for c in cipher:
                print(f"[*] {c} - {classificatie}")
    
# demo
find_tls('nu.nl')
# find_tls('vpn.phoenixus.com')
# find_tls('martiniziekenhuis.nl')
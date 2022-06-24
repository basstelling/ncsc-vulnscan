import subprocess
from src.ncsc_config import read_config

def find_tls(url):
    if "https://www." in url:
        url = url[12:]
    elif "http://www." in url:
        url = url[11:]
    elif "https://" in url:
        url = url[8:]
    elif "http://" in url:
        url = url[7:]
    
    if url[-1] == '/':
        url = url[:-1]
    nmap_command = 'nmap --script ssl-enum-ciphers -p 443 ' + url
    output = subprocess.getoutput(nmap_command)
    output_lines = output.splitlines()

    good_tls_ciphers = read_config('Cipher Suites', 'Goed').split('\n')
    ok_tls_ciphers = read_config('Cipher Suites', 'Voldoende').split('\n')
    bad_tls_ciphers = read_config('Cipher Suites', 'Uit te faseren').split('\n')
    good_tls_versions = read_config('TLS', 'Goed').split('\n')
    ok_tls_versions = read_config('TLS', 'Voldoende').split('\n')
    bad_tls_versions = read_config('TLS', 'Uit te faseren').split('\n')
    vulnerable_ssl_versions = read_config('TLS', 'Onvoldoende').split('\n')

    used_ciphers = {"Goed":[], "Voldoende":[], "Uit te faseren":[]}
    used_tls_versions = {"Goed":[], "Voldoende":[], "Uit te faseren":[], "Onvoldoende":[]}

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
                    used_ciphers['Uit te faseren'] += [cipher]

        for tls in good_tls_versions:
            if tls in line:
                if 'Goed' in used_tls_versions:
                    used_tls_versions['Goed'].append(str(tls))
        for tls in ok_tls_versions:
            if tls in line:
                if 'Voldoende' in used_tls_versions:
                    used_tls_versions['Voldoende'].append(str(tls))
        for tls in bad_tls_versions:
            if tls in line:
                if 'Goed' in used_tls_versions:
                    used_tls_versions['Uit te faseren'].append(str(tls))
        for tls in vulnerable_ssl_versions:
            if tls in line:
                if 'Goed' in used_tls_versions:
                    used_tls_versions['Onvoldoende'].append(str(tls))

    print("[i]",url,"ondersteunt de volgende TLS-versies:")
    for classificatie, version in used_tls_versions.items():
        if len(version) != 0:
            for v in version:
                print(f'[*] {v} - {classificatie}')
    length = sum([1 if isinstance(used_ciphers[a], (str, int))
            else len(used_ciphers[a])
            for a in used_ciphers])
    print(f"[i] {url} maakt gebruik van {length} ciphers.")

    for classificatie, cipher in used_ciphers.items():
        if len(cipher) != 0:
            for c in cipher:
                print(f"[*] {c} - {classificatie}")
    
# demo
# find_tls('nu.nl')
# find_tls('https://vpn.phoenixus.com/')
# find_tls('martiniziekenhuis.nl')
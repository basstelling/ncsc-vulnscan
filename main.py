from datetime import date, datetime
import socket
import subprocess
import sys
import requests
import os
from urllib.parse import urlparse
from src.ncsc_config import get_boolean
from src.port_scan import port_scan
from src.header_scan import header_checker
from src.tls_scan import find_tls


now = datetime.now()
current_time = now.strftime("%H-%M-%S")
date_now = str(date.today()) + "--" + str(current_time)

# check if data needs to be saved according to the config
saveData = get_boolean("Export data")


def get_resp():
    return resp

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def xss_format(url):
    xss_command = 'python src\\xsscrapy.py -u %s' % url
    xss_output = subprocess.getoutput(xss_command)
    xss_domain = urlparse(url).netloc.replace('www.', '').split(':')[0]

    path_vuln = 'Scans/XSS/XSS-scan--' + xss_domain + '--.txt'
    path_log = f'Scans/XSS/Logging/Log-XSS--' + xss_domain + '--.txt'

    path_vuln_gen = f'Scans/Volledige scans/General-scan--{xss_domain}--{date_now}.txt'
    path_log_gen = f'Scans/Volledige scans/Logging/Log-General-XSS--{xss_domain}--{date_now}.txt'

    with open(path_vuln, 'r') as vuln:
        data = vuln.read()
    
    with open(path_vuln, 'w') as modified:
        modified.write(f"[!] Mogelijke XSS-kwetsbaarheden op {xss_domain}:\n---" + data)

    with open(path_log,'w+') as f:
        f.write(xss_output)

    if get_resp() == '6':
        path_save_data = path_vuln_gen
        with open(path_vuln_gen, 'w+') as general:
            general.write(data)
            os.remove(path_vuln)
        
        with open(path_log_gen, 'w+') as log_general:
            log_general.write(xss_output)
            os.remove(path_log)
        
    if get_resp() == '5':
        path_save_data = f'Scans/XSS/XSS-scan--{xss_domain}--' + date_now +  '.txt'
        os.rename(path_vuln, f'Scans/XSS/XSS-scan--{xss_domain}--' + date_now +  '.txt')
        os.rename(path_log, f'Scans/XSS/Logging/Log-XSS--{xss_domain}--' + date_now +  '.txt')
    
    if saveData == False:
        with open(path_save_data, 'r') as r:
            xss_resultaten = r.read()
            print(xss_resultaten)
        
        os.remove(path_save_data)


def check_url(url):
    try:
        request = requests.get(url)
        if request.status_code == 200:
            return True
        else:
            return False
    except:
        return False

try:
    cls()
    resp = input("[i] Welkom bij deze tool. Welke scan wilt u uitvoeren? Typ 'all' voor alle onderstaande. \n"
                "[i] \t1) Portscan\t\t\t4) Patch Enumeration\n"
                "[i] \t2) HTTP response header\t\t5) XSS- & SQLi-spider\n"
                "[i] \t3) TLS-versie herkennen\t\t6) Volledige scan\n"
                "[?] Voer het nummer in van de scan die u wilt uitvoeren: ")

    if resp == '1':
        host = input("[?] Voer het te scannen IP adres in: ")
        ports = input("[?] Voer de te scannen poort(en) in: ")
        if saveData == True:
            with open(r'Scans/Portscan/Port scan '+ host + '-' +date_now + ".txt",'w') as f:
                sys.stdout = f
                cls()
                port_scan(host, ports)
        else:
            port_scan(host, ports)

    elif resp == '2':
        url = input("[?] Voer de URL in waarvan u de headers wilt analyseren: ")
        if saveData == True:
            with open(r'Scans/HTTP headers/Header scan ' + urlparse(url).netloc + '-' + date_now + ".txt",'w') as f:
                sys.stdout = f
                cls()
                header_checker(url)
        else:
            header_checker(url)

    elif resp == '3':
        url = input("[?] Voer de URL in waarvan u de ondersteunde TLS-versies wilt herkennen: ")
        if saveData == True:
            with open(r'Scans/TLS/TLS scan ' + urlparse(url).netloc + '-' + date_now + ".txt",'w') as f:
                sys.stdout = f
                cls()
                find_tls(url)
        else:
            find_tls(url)

    elif resp == '4':
            path = "src/data/systeminfo/"
            filename = input("[?] Wat is de naam van het systeminfo bestand?\n[?] " + path)
            systeminfo_path = path + filename
            update_wesng_command = 'python src/wesng/wes.py --update'
            enumeration_command = 'python src/wesng/wes.py %s' % systeminfo_path
            update_output = subprocess.getoutput(update_wesng_command)
            output = subprocess.getoutput(enumeration_command)
            if saveData == True:
                with open(r'Scans/Patch Enumeration/Patch enumeration '+ filename + '-' + date_now + ".txt",'w', encoding='utf-8') as f:
                    sys.stdout = f
                    cls()
                    print(output)
            else:
                print(output)

    elif resp == '5':
        xss_url = input("[?] Voer de URL in die u op XSS wilt toetsen: ")
        if check_url(xss_url) == True:
            xss_format(xss_url)
        else:
            print(f"[!] De ingevoerde URL {xss_url} bestaat niet of is offline. Controleer de URL en probeer het opnieuw.")

    elif resp == '6':
        url = input("[?] Voer de URL van de website die u wilt scannen: ")
        if check_url(url) == True:
            stripped_url = urlparse(url).netloc
            ip = socket.gethostbyname(stripped_url)

            print("[i] Scan wordt uitgevoerd...")
            if saveData == True:
                with open(r'Scans/Volledige scans/General-scan--' + stripped_url + '--' + date_now + '.txt', 'w') as f:
                    sys.stdout = f
                    f.write("[i] RESULTATEN VAN DE PORTSCAN:\n")
                    print("\t", port_scan('127.0.0.1', '1-11000'))
                    f.write("\n[i] RESULTATEN VAN DE HTTP HEADER CONTROLE: \n")
                    print("\t",header_checker(url))
                    f.write("\n[i] RESULTATEN VAN DE TLS-SCAN:\n")
                    print("\t",find_tls(url))
                    f.write("\n[i] MOGELIJKE XSS-KWETSBAARHEDEN: \n")
                    xss_format(url)
                
            else:
                print("Poort scan:")
                print(port_scan('127.0.0.1', '1-100'))
                print("\nHTTP response header checker:")
                print(header_checker(url))
                print("\nTLS-versies en ciphers controleren:")
                print(find_tls(url))
                print("\nXSS-scan uitvoeren:")
                print(xss_format(url))
                
    
        else: 
            print(f"[!] De ingevoerde URL {url} bestaat niet of is offline. Controleer de URL en probeer het opnieuw.")

except KeyboardInterrupt as e:
    print('\n[!] Scan beëindigd.', e)
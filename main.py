from datetime import date
from email.quoprimime import header_check
import sys
from ncsc_config import get_boolean, read_config
from port_scan import port_scan
from header_scan import header_checker
from tls_scan import find_tls
from xss_scanner import scan_xss
from crawler import crawl
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

date = str(date.today())
# check if data needs to be saved according to the config
saveData = get_boolean("Export data", "boolean")


try:
    cls()
    resp = input("[i] Welkom bij deze tool. Welke scan wilt u uitvoeren? Typ 'all' voor alle onderstaande. \n"
                "[i] \t1) Portscan\n"
                "[i] \t2) HTTP response header\n"
                "[i] \t3) TLS-versie herkennen\n"
                "[i] \t4) XSS-scannner\n"
                "[i] \t5) Web crawler\n"
                "[?] Voer het nummer in van de scan die u wilt uitvoeren: ")
    # save = input("[?] Wilt u de output opslaan? Y/n ")
    # if save == ('Y' or 'y'):
    #     saveData = True
    #     try:
    #         dir_name = "Scans"
    #         os.mkdir(dir_name)
    #         print("[i] Scans directory aangemaakt; hierin zal de output opgeslagen worden.")
    #     except FileExistsError as e:
    #         print("[i] Directory '%s' bestaat al, verder gaan met scan..." % dir_name)

    if resp == '1':
        host = input("[?] Voer het te scannen IP adres in: ")
        ports = input("[?] Voer de te scannen poort(en) in: ")
        if saveData == True:
            with open(r'Scans/Port scan '+date,'w') as f:
                sys.stdout = f
                cls()
                port_scan(host, ports)
        else:
            port_scan(host, ports)

    elif resp == '2':
        url = input("[?] Voer de URL in waarvan u de headers wilt analyseren: ")
        if saveData == True:
            with open(r'Scans/Header scan '+date,'w') as f:
                sys.stdout = f
                cls()
                header_checker(url)
        else:
            header_checker(url)

    elif resp == '3':
        url = input("[?] Voer de URL in waarvan u de ondersteunde TLS-versies wilt herkennen: ")
        if saveData == True:
            with open(r'Scans/TLS scan '+date,'w') as f:
                sys.stdout = f
                cls()
                find_tls(url)
        else:
            find_tls(url)

    elif resp == '4':
        url = input("[?] Voer de URL in die u op XSS wilt toetsen: ")
        if saveData == True:
            with open(r'Scans/XSS scan '+date,'w', encoding='utf-8') as f:
                sys.stdout = f
                cls()
                scan_xss(url)
        else:
            scan_xss(url)
    
    elif resp == '5':
        url = input("[?] Voer de URL in die u wilt crawlen: ")
        print(crawl(url, '/'), len(crawl(url, '/')))
        

    else:
        host = input("[?] Voer het te scannen IP adres in: ")
        ports = input("[?] Voer de te scannen poort(en) in: ")
        url = input("[?] Voer de URL van de website die u wilt scannen: ")
        print("[i] Scan wordt uitgevoerd...")
        if saveData == True:
            with open(r'Scans/General scan '+date,'w') as f:
                sys.stdout = f
                port_scan(host, ports)
                header_checker(url)
                find_tls(url)
                scan_xss(url)
        else:
            port_scan(host, ports)
            header_checker(url)
            find_tls(url)
            scan_xss(url)
    
    # export = input("Wilt u de data opslaan? Y/n ")
    # if export == 'y':
    #     file_name = 'scan_' + str(date.today())
    #     os.system('python3 ')
        
    #     with open(file_name, 'w') as f:
    #         f.write(str(port_scan))

except KeyboardInterrupt as e:
    print('\n[!] Scan beëindigd.', e)


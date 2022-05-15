from email.quoprimime import header_check
from port_scan import port_scan
from header_scan import header_checker
from tls_scan import find_tls
from xss_scanner import scan_xss
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

try:
    cls()
    resp = input("[i] Welkom bij deze tool. Welke scan wilt u uitvoeren? Typ 'all' voor alle onderstaande. \n"
                "[i] \t1) Portscan\n"
                "[i] \t2) HTTP response header\n"
                "[i] \t3) TLS-versie herkennen\n"
                "[i] \t4) XSS-scannner\n"
                "[?] Voer het nummer in van de scan die u wilt uitvoeren: ")

    if resp == '1':
        host = input("[?] Voer het te scannen IP adres in: ")
        ports = input("[?] Voer de te scannen poort(en) in: ")
        cls()
        port_scan(host, ports)

    elif resp == '2':
        url = input("[?] Voer de URL in waarvan u de headers wilt analyseren: ")
        cls()
        header_checker(url)

    elif resp == '3':
        url = input("[?] Voer de URL in waarvan u de ondersteunde TLS-versies wilt herkennen: ")
        cls()
        find_tls(url)

    elif resp == '4':
        url = input("[?] Voer de URL in die u op XSS wilt scannen: ")
        cls()
        scan_xss(url)

    else:
        host = input("[?] Voer het te scannen IP adres in: ")
        ports = input("[?] Voer de te scannen poort(en) in: ")
        url = input("[?] Voer de URL van de website die u wilt scannen: ")
        port_scan(host, ports)
        header_checker(url)
        find_tls(url)
    
    # export = input("Wilt u de data opslaan? Y/n ")
    # if export == 'y':
    #         os.system('python3 main.py > output.txt')


except KeyboardInterrupt as e:
    print('\n[!] Scan beëindigd.', e)

    # header_checker('https://vulnerable-website.com')
    # header_checker('https://www.python.org')


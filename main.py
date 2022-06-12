from datetime import date
from email.quoprimime import header_check
import subprocess
import sys
from src.ncsc_config import read_config, set_config
from src.port_scan import port_scan
from src.header_scan import header_checker
from src.tls_scan import find_tls
from src.xss_scanner import scan_xss
import src.windows_exploit_suggester
# from crawler import crawl
import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

date = str(date.today())
# check of config.ini bestaat

if os.path.exists('src/data/ncsc_config.ini') == False:
    set_config()
else:
    print("[i] Config bestaat, verder gaan...")


# check if data needs to be saved according to the config
saveData = read_config("Export data", "boolean")


try:
    # cls()
    resp = input("[i] Welkom bij deze tool. Welke scan wilt u uitvoeren? Typ 'all' voor alle onderstaande. \n"
                "[i] \t1) Portscan\t\t\t4) Patch Enumeration\n"
                "[i] \t2) HTTP response header\t\t5) XSS- & SQLi-spider\n"
                "[i] \t3) TLS-versie herkennen\n"
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
            with open(r'src/Scans/Port scan '+date + ".txt",'w') as f:
                sys.stdout = f
                cls()
                port_scan(host, ports)
        else:
            port_scan(host, ports)

    elif resp == '2':
        url = input("[?] Voer de URL in waarvan u de headers wilt analyseren: ")
        if saveData == True:
            with open(r'src/Scans/Header scan '+date + ".txt",'w') as f:
                sys.stdout = f
                cls()
                header_checker(url)
        else:
            header_checker(url)

    elif resp == '3':
        url = input("[?] Voer de URL in waarvan u de ondersteunde TLS-versies wilt herkennen: ")
        if saveData == True:
            with open(r'src/Scans/TLS scan '+date + ".txt",'w') as f:
                sys.stdout = f
                cls()
                find_tls(url)
        else:
            find_tls(url)

    elif resp == '4':
        # choice = input("[?] Wilt u de websites in de config toetsen, of wilt u een domein vanaf een URL toetsen?\n[?] ")
        # print(type(choice))
        # print(choice.strip() == ('config' or 'conf' or 'configuration'))

        # if choice.strip() == ('config' or 'conf' or 'configuration'):
            # websites = []
            # config_websites = read_config("Te scannen websites", "websites")
            # print(config_websites)
        # elif choice.strip() == ('URL' or 'crawler' or 'domein'):
            path = "src/data/systeminfo/"
            # bulletin_path = path + input("[?] Wat is de naam van het bestand met security bulletins?\n")
            systeminfo_path = path + input("[?] Wat is de naam van het systeminfo bestand?\n[?] ")
            update_wesng_command = 'python src/wesng/wes.py --update'
            enumeration_command = 'python src/wesng/wes.py %s' % systeminfo_path
            update_output = subprocess.getoutput(update_wesng_command)
            output = subprocess.getoutput(enumeration_command)
            if saveData == True:
                with open(r'src/Scans/Patch enumeration '+date + ".txt",'w', encoding='utf-8') as f:
                    sys.stdout = f
                    cls()
                    print(output)
            else:
                print(output)
        # else:
        #    print("[!] Geen geldige keuze gegeven; kies tussen 'config' en 'url'.")

    elif resp == '5':
        url = input("[?] Voer de URL in die u op XSS wilt toetsen: ")
        if saveData == True:
            with open(r'src/Scans/XSS scan '+date + ".txt",'w', encoding='utf-8') as f:
                sys.stdout = f
                cls()
                scan_xss(url)
        else:
            scan_xss(url)

    elif resp == 'set conf':
        set_config()

    else:
        host = input("[?] Voer het te scannen IP adres in: ")
        ports = input("[?] Voer de te scannen poort(en) in: ")
        url = input("[?] Voer de URL van de website die u wilt scannen: ")
        print("[i] Scan wordt uitgevoerd...")
        if saveData == True:
            with open(r'Scans/General scan '+date, + ".txt", 'w') as f:
                sys.stdout = f
                print("Poort scan:")
                port_scan(host, ports)
                print("\nHTTP response header checker:")
                header_checker(url)
                print("\nTLS-versies en ciphers controleren:")
                find_tls(url)
                print("\nControleren op XSS:")
                scan_xss(url)
        else:
            print("Poort scan:")
            port_scan(host, ports)
            print("\nHTTP response header checker:")
            header_checker(url)
            print("\nTLS-versies en ciphers controleren:")
            find_tls(url)
            print("\nXSS-scan uitvoeren:")
            scan_xss(url)
    
    # export = input("Wilt u de data opslaan? Y/n ")
    # if export == 'y':
    #     file_name = 'scan_' + str(date.today())
    #     os.system('python3 ')
        
    #     with open(file_name, 'w') as f:
    #         f.write(str(port_scan))

except KeyboardInterrupt as e:
    print('\n[!] Scan beëindigd.', e)


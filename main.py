from portScan import portScan
from headerScan import headerChecker

resp = input("Welkom bij deze tool. Voer het nummer in van de actie die u wilt uitvoeren. \n\n"
            "1) Portscan\n"
            "2) Web Header Configuration\n")

if resp == '1':
    host = input("Voer het te scannen IP adres in:\n")
    ports = input("Voer de te scannen poort(en) in:\n")
    portScan(host, ports)

if resp == '2':
    url = input("Voer de URL in waarvan u de headers wilt analyseren: \n")
    headerChecker(url)

    # headerChecker('https://vulnerable-website.com')
    # headerChecker('https://www.python.org')


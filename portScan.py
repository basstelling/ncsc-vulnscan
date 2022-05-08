from unicodedata import name
import socket
import nmap
import time

def portScan(target,ports):
    # portScanner object aanmaken
    try:
        scanner = nmap.PortScanner()
        startTime = time.time()
        # scannen van hosts op bepaalde poorten volgens bepaalde nmap flags
        scanner.scan(target, ports=ports, arguments='-T4')
        hostlist = scanner.all_hosts()
        # door alle gescande hosts loopen
        for host in hostlist:
            try:
                # per host het ip en hostname ophalen en printen waar mogelijk
                print('-----------------------')
                print('Host : %s (%s)' % (host, scanner[host].hostname()))
                for protocol in scanner[host].all_protocols():
                    print('-----')
                    print('Protocol : %s' % protocol)

                    portList = sorted(scanner[host][protocol])
                    for port in portList:
                            print('port : %s\tstatus : %s\t service : %s' % (port, scanner[host][protocol][port]['state'], scanner[host][protocol][port]['name']))
                    print('\n')
            except KeyError as e:
                print(e)
                return False
    except nmap.PortScannerError as b:
        print("Er is geen installatie van Nmap gevonden in de omgevingsvariabelen van deze machine.\n", b)
        return False

    # totale tijd teruggeven
    totalTime = time.time() - startTime
    print('-----------------------')
    print('De scan heeft', format(totalTime, ".4f"), 'seconden geduurd.')
    print('-----------------------')

# portScan('192.168.1.1/26', '22-23')
from unicodedata import name
import socket
import nmap
import time

def port_scan(target,ports):
    # portScanner object aanmaken
    try:
        scanner = nmap.PortScanner()
        startTime = time.time()
        # scannen van hosts op bepaalde poorten volgens bepaalde nmap flags
        scanner.scan(target, ports=ports, arguments='-T4 -A -v')
        hostlist = scanner.all_hosts()
        # door alle gescande hosts loopen
        for host in hostlist:
            try:
                if len(scanner[host].hostname()) != 0:
                    hostname = scanner[host].hostname()
                else:
                    hostname = 'Hostname unknown'
                # per host het ip en hostname ophalen en printen waar mogelijk
                print('-----------------------')
                print('Host : %s (%s)' % (host, hostname))
                for protocol in scanner[host].all_protocols():
                    print('-----')
                    print('Protocol : %s' % protocol)

                    portList = sorted(scanner[host][protocol])
                    for port in portList:
                            print('port : %s\tstatus : %s\tservice : %s' % (port, scanner[host][protocol][port]['state'], scanner[host][protocol][port]['name']))
                    print('\n')
            except KeyError as e:
                print(e)
                return False
    except nmap.PortScannerError as b:
        print("Er is geen installatie van Nmap gevonden in de omgevingsvariabelen van deze machine.\n", b)
        return False
    except KeyboardInterrupt as c:
        print('Scan beëindigd.')
        return False

    # totale tijd teruggeven
    totalTime = time.time() - startTime
    totalHosts = len(hostlist)

    print('-----------------------')
    print('De scan heeft', format(totalTime, ".2f"), 'seconden geduurd.')
    print(totalHosts, 'host(s) gescand.')
    print('-----------------------')

# portScan('localhost', '1-5')
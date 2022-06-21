from unicodedata import name
import nmap
import time

def port_scan(target,ports):
    # portScanner object aanmaken
    try:
        scanner = nmap.PortScanner()
        startTime = time.time()
        # scannen van hosts op bepaalde poorten volgens bepaalde nmap flags
        scanner.scan(target, ports=ports, arguments='-T3 -v')
        hostlist = scanner.all_hosts()
        # door alle gescande hosts loopen
        for host in hostlist:
            try:
                if len(scanner[host].hostname()) != 0:
                    hostname = scanner[host].hostname()
                else:
                    hostname = 'Hostname onbekend'
                # per host het ip en hostname ophalen en printen waar mogelijk
                print('-----------------------')
                print('[i] Host: %s (%s)' % (host, hostname))
                print('[i] Status: %s' % scanner[host].state())
                for protocol in scanner[host].all_protocols():
                    print('-----')
                    print('[+] Protocol : %s' % protocol)

                    portList = sorted(scanner[host][protocol])
                    for port in portList:

                            port_string = ('\t- poort: {:5}' +
                            '\t\tstatus: {:8}' +
                            '\tservice: {}')
                            
                            print((port_string).format(port, scanner[host][protocol][port]['state'], scanner[host][protocol][port]['name']))
            except KeyError as e:
                print(e)
                return False
    except nmap.PortScannerError as b:
        print("[!] Er is geen installatie van Nmap gevonden in de omgevingsvariabelen van deze machine.\n", b)
        return False
    except KeyboardInterrupt as c:
        print('[!] Scan beëindigd.')
        return False

    # totale tijd teruggeven
    totalTime = time.time() - startTime
    totalHosts = len(hostlist)

    print('-----------------------')
    print(f'[i] De scan heeft {format(totalTime, ".2f")} seconden geduurd.')
    print(f'[i] {totalHosts} host(s) gescand op poorten {ports}.')

# demo
# port_scan('localhost', '1-10000')
# port_scan('localhost', '80, 443')

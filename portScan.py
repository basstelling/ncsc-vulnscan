from multiprocessing.sharedctypes import Value
import nmap
import ipaddress
from datetime import datetime

def portScan(target):
    # portScanner object aanmaken
    scanner = nmap.PortScanner()
    # scannen van hosts op bepaalde poorten volgens bepaalde nmap flags
    scanner.scan(target, ports='22-443', arguments='-T4')
    hostlist = scanner.all_hosts()
    startTime = datetime.now()

    # door alle gescande hosts loopen
    for host in hostlist:
        try:
            # per host ip + host name printen waar mogelijk
            print('-----------------------')
            print('Host : %s (%s)' % (host, scanner[host].hostname()))
            for protocol in scanner[host].all_protocols():
                print('-----')
                print('Protocol: %s' % protocol)

                portList = sorted(scanner[host][protocol])
                for port in portList:
                    print('port: %s\tstate : %s' % (port, scanner[host][protocol][port]['state']))
        except KeyError as e:
            print(e)
            return False

        # tijd teruggeven
        totalTime = datetime.now() - startTime
        print('-----------------------')
        print('De scan heeft', totalTime, 'minuten geduurd.')
        print('-----------------------')
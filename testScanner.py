import nmap
from datetime import datetime


def testScanner(target):
    scanner = nmap.PortScanner()
    scanner.scan(target, ports='22-443', arguments='-T4')
    hostlist = scanner.all_hosts()

    for host in hostlist:
        try:
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

testScanner('127.0.0.1')


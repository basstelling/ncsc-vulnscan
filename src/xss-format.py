from datetime import datetime, date
import subprocess
import sys
from urllib.parse import urlparse


now = datetime.now()
current_time = now.strftime("%H-%M")
date_now = str(date.today()) + "--" + str(current_time)

def xss_format(url, resp):
    xss_command = 'python src/xsscrapy.py -u %s' % url
    xss_output = subprocess.getoutput(xss_command)
    xss_domain = urlparse(url).netloc
    # url = input("[?] Voer de URL in die u op XSS wilt toetsen: ")
    # print(type(saveData))
    if resp == '6':
        path_vuln = f'Scans/Volledige scans/General-scan-{xss_domain}--' + date_now + ".txt"
        path_log = f'Scans/Volledige scans/Logging/Log-XSS-{xss_domain}--' + date_now + ".txt"
    else:
        path_vuln = f'Scans/XSS/XSS-scan-{xss_domain}--' + date_now + ".txt"
        path_log = f'Scans/XSS/Logging/Log-XSS-{xss_domain}--' + date_now + ".txt"
        
    with open(path_vuln, 'w+') as original: 
        # original.write(xss_output)
        data = str(original.read())
    with open(path_vuln, 'w') as modified: 
        if len(data) != 0:
            modified.write(f"[i] Mogelijke XSS-kwetsbaarheden op {xss_domain}:\n---" + data)
        else:
            modified.write("[!] Geen XSS-kwetsbaarheden gevonden; zie logs voor details." + data)
    with open(path_log + ".txt",'wb+') as f:
            sys.stdout = f
            #     # cls()
            #     # f.write("[i] Resultaten van de XSS-scan:")
            f.write(xss_output, encoding='utf-8')



xss_command = 'python src/xsscrapy.py -u %s' % 'https://xss-game.appspot.com/level1/'
xss_output = subprocess.getoutput(xss_command)
print(xss_output)
xss_domain = urlparse('https://xss-game.appspot.com/level1/').netloc
print(xss_domain)

path_vuln = f'Scans/Volledige scans/General-scan-{xss_domain}--' + date_now + ".txt"
path_log = f'Scans/Volledige scans/Logging/Log-XSS-{xss_domain}--' + date_now + ".txt"
print(path_vuln, "\n", path_log)

with open(path_vuln, 'w+') as original: 
        # original.write(xss_output)
        data = original.read()
        print(data)

with open(path_vuln, 'w') as modified: 
    modified.write(f"[i] Mogelijke XSS-kwetsbaarheden op {xss_domain}:\n---" + data)
    # else:
    #     modified.write("[!] Geen XSS-kwetsbaarheden gevonden; zie logs voor details." + data)

with open(path_log + ".txt",'w+') as f:
        sys.stdout = f
        #     # cls()
        #     # f.write("[i] Resultaten van de XSS-scan:")
        print(xss_output)
# ncsc-vulnscan
NCSC-Vulnscan is een tool die gebaseerd is op de normen van het NCSC. Aan de hand van diverse tests kan de tool de toetsing van bepaalde normen deels geautomatiseerd uitvoeren zodat IT-auditors meer zekerheid kunnen hebben over de mate van veiligheid die een webapplicatie heeft m.b.t de gestelde normen van het NCSC.

## Gebruik
  1) Installeer Python, Nmap en Git. 
  - Python kan geïnstalleerd worden op https://www.python.org/ -- het is hierbij belangrijk dat Python aan de PATH-variabelen toevoegd wordt!
  - Nmap kan geïnstalleerd worden op https://nmap.org/download.html
  - Git kan geïnstalleerd worden op https://git-scm.com/download/win -- normaliter niet nodig, maar omdat PyPi momenteel niet de juiste versie van Pybloom installeert moet hij via Git opgehaald worden.
  2) Installeer Pybloom **vanuit de vulnscan directory** door het volgende commando uit te voeren in de CMD:
  ```shell
  pip install -e git+https://github.com/jaybaird/python-bloomfilter.git#egg=pybloom
  ```
  3) Installeer de benodigde modules van de tool met het volgende CMD-commando:
  ```shell
  pip install -r requirements.txt
  ```
  4) Run de tool door te navigeren naar de vulnscan directory en het volgende commando uit te voeren:
  ```shell
  python main.py
  ```
  Resultaat:
  
 ![cropped_cmd](https://user-images.githubusercontent.com/43985189/175276700-b2171106-4a18-4da1-9327-a209b0fe9c91.png)
 
## Functies
### 1) Port Scan
De poortscanner functie maakt gebruik van Nmap. Hierbij kan een IP-adres, maar ook een URL opgegeven worden; van de URL wordt dan het publieke IP opgehaald en dit IP zal dan gescand worden.

### 2) HTTP-header response checker
De HTTP-header response checker controleert op de inhoud van waardes volgens het NCSC. Een belangrijk punt: de tool merkt nonces niet op, omdat deze achter een log-in pas meegegeven worden. Bij een bevinding van unsafe-evals en unsafe-inlines binnen de CSP-header is het daarom belangrijk om ter controle zelf nog in te loggen.

### 3) TLS-versie herkennen
TLS-versies worden herkend d.m.v de waarden die meegegeven worden vanuit het ncsc_configs.ini bestand. Op het moment van schrijven (23-06-2022) zijn deze actueel, maar mochten hier veranderingen in komen dan hoeven alleen de waarden in het config bestand vervangen te worden. Het is hierbij belangrijk om de huidige structuur aan te houden.
 
### 4) Uitvoeren van Patch Enumeration (WES-NG)
Om gebruik te maken van de patch enumeration functie, moet er een systeminfo.txt file aanwezig zijn. Deze kunnen opgeslagen worden onder src/data/systeminfo als .txt bestand. Tijdens het uitvoeren van het programma hoeft daarna alleen maar de naam van het bestand ingevoerd te worden, waarna geïnstalleerde KBs worden vergeleken. Voor het uitlezen van de resultaten, gebruik https://github.com/bitsadmin/wesng/wiki/Eliminating-false-positives als hulpmiddel.

### 5) XSS- en SQLi-spider
De XSS- en SQLi-spider functie is geïmplementeerd met XSScrapy. Deze module controleert, zoals de naam zegt, d.m.v Scrapy op XSS- en SQLi-kwetsbaarheden binnen een webapplicatie. Voor deze functie hoeft alleen een link ingevoerd te worden.

### 6) Volledige scan
De volledige scan voert alle bovenstaande functies uit behalve functie 4.

### ncsc_config.ini
In dit bestand worden classificaties van ciphers en TLS-versies opgeslagen. Ook wordt hier aangegeven of de data uitgeschreven moet worden in de terminal of opgeslagen in een .txt bestand. Om dit aan te passen, hoeft alleen de saveData variabele op True (data opslaan) of False (data uitschrijven in terminal) gezet te worden.

License XSScrapy
-------

Copyright (c) 2014, Dan McInerney
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
* Neither the name of Dan McInerney nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


## License WES-NG
Copyright 2019 Arris Huijgen

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

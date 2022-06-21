import requests

def header_checker(url):
    try:
        # response header aanvragen
        resp = requests.get(url)
        if resp.status_code == 200:
            print('-----------------------')
            print(f'[i] Response header opgehaald van {url}')
            print('[i] Controleren op NCSC waarden...')
            print('-----')

            # X-Content-Type-Options
            # nosniff 
            try:
                x_content_type = resp.headers['X-Content-Type-Options']
                if 'nosniff' in x_content_type:
                    print('[*] X-Content-Type-Options staat juist ingesteld volgens de aanbevolen waarden van het NCSC.')
                else:
                    print('[!] X-Content-Type-Options voldoet niet aan de eisen van het NCSC.')
            except:
                print('[!] X-Content-Type-Options mist.')

            # Content-Security-Policy
            # unsafe-eval/unsafe-inline + nonce = goed
            # géén unsafe-eval/unsafe-inline = goed
            # unsafe-eval = fout
            try:
                content_security = resp.headers['Content-Security-Policy']
                # print(content_security)
                if 'unsafe-eval' or 'unsafe-inline' in content_security:
                    if 'nonce' in content_security:
                        print('[*] Content-Security-Policy maakt gebruik van unsafe-eval of unsafe-inline met nonce.')
                    else:
                        print(f'[!] Content-Security-Policy maakt gebruik van unsafe-eval of unsafe-inline, mogelijk zonder nonce; controleer dit door in te loggen op {url}.')
                else:
                    print(f'[*] {url} maakt geen gebruik van \'unsafe-eval\' of \'unsafe-inline\'.')
            except:
                print('[!] Content-Security-Policy mist.')

            # Referrer-Policy
            # same-origin of no-referrer
            try:
                referrer_policy = resp.headers['Referrer-Policy']
                # print(referrer_policy)
                if 'same-origin' and 'no-referrer' in referrer_policy:
                    print('[*] Referrer-Policy maakt gebruik van same-origin én no-referrer.')
                elif 'same-origin' in referrer_policy:
                    print('[*] Referrer-Policy maakt gebruik van same-origin.')
                else:
                    print('[!] Referrer-Policy maakt geen gebruik van same-origin en staat niet ingesteld volgens de aanbevolen waarden van het NCSC.')
            except:
                print('[!] Referrer-Policy mist.')

            # Strict-Transport-Security
            # max-age=31536000 of includeSubdomains
            try:
                strict_transport_security = resp.headers['Strict-Transport-Security']
                # print(strict_transport_security)
                if 'max-age=31536000'  and 'includeSubdomains' in strict_transport_security:
                    print('[*] Strict-Transport voldoet aan de eisen van het NCSC, en heeft de headers max-age en includeSubdomains juist ingesteld. ')
            except:
                print('[!] Strict-Transport-Security mist.')

            # X-Frame-Options
            # deny of sameorigin, één van beiden
            try:
                x_frame_options = resp.headers['X-Frame-Options']
                # print(x_frame_options)
                if 'deny' or 'sameorigin' in x_frame_options:
                    print('[*] X-Frame-Options voldoet aan de eisen van het NCSC, en maakt gebruik van deny of sameorigin.')
            except:
                print('[!] X-Frame-Options mist.')
            print('------------')

            # controleren op verschillende requestmethodes & mogelijk onnodige data binnen de response header
            reqmethods = ['GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'OPTIONS', 'TRACE', 'CONNECT', 'TEST']
            headers = ['Server', 'Date', 'Via', 'X-Powered-By', 'X-Country-Code']

            print('\nControleren op overbodige request methodes:')
            print('-----')
            for method in reqmethods:
                resp = requests.request(method, url)
                if resp.status_code == 200:
                        print('[*] Ophalen van response header met request method', method, 'is mogelijk.')
            # print('------------\n')
            
            # print(resp.headers)
            # for header in headers:
            #     if header in resp.headers:
            #         print(header, resp.headers[header])
            #         print('Controleren op mogelijk overbodige headers:')
            #         print('-----')
            #         for h in headers:
            #             # print(headers)
            #             try:
            #                 result = resp.headers[h]
            #                 if len(result) != 0:
            #                     print('[i] %s: %s' % (h, result))
            #                 else:
            #                     print('[i] Geen overbodige headers gevonden.')
            #             except Exception as e:
            #                 return False
            #         print('------------')

        else:
            print('[!] HTTP header niet kunnen ophalen.')


    except requests.exceptions.SSLError as g:
        print('[!] Website maakt gebruik van een ongeldig SSL certificaat, waardoor de response header niet opgehaald kon worden.')

# demo
# header_checker('https://www.martiniziekenhuis.nl')
# header_checker('https://www.python.org')
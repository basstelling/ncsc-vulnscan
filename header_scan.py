from email.policy import strict
import requests

def header_checker(url):
    try:
        # response header aanvragen
        resp = requests.get(url)
        if resp.status_code == 200:
            print('-----------------------')
            print('[i] Response header opgehaald van', url)
            print('[i] Controleren op NOREA waarden...')
            print('-----')

            # X-Content-Type-Options
            # nosniff 
            try:
                x_content_type = resp.headers['X-Content-Type-Options']
                if 'nosniff' in x_content_type:
                    print('[*] X-Content-Type-Options staat juist ingesteld volgens de aanbevolen waarden van NOREA.')
                else:
                    print('[!] X-Content-Type-Options voldoet niet aan de eisen van NOREA.')
            except:
                print('[!] X-Content-Type-Options mist.')

            # Content-Security-Policy
            # unsafe-eval/unsafe-inline + nonce = goed
            # géén unsafe-eval/unsafe-inline = goed
            # unsafe-eval = fout
            try:
                content_security = resp.headers['Content-Security-Policy']
                # print(content_security)
                if (('unsafe-eval' and 'unsafe-inline') and ('nonce' in content_security) in content_security):
                    print('[*] Content-Security-Policy maakt gebruik van unsafe-eval of unsafe-inline met een nonce.')
                elif ('unsafe-eval' and 'unsafe-inline') not in content_security:
                    print('[*] Content-Security-Policy maakt geen gebruik van unsafe-eval of unsafe-inline.')
                else:
                    print('[!] Content-Security-Policy voldoet niet aan de eisen van NOREA.')
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
                    print('[!] Referrer-Policy maakt geen gebruik van same-origin en staat niet ingesteld volgens de aanbevolen waarden van NOREA.')
            except:
                print('[!] Referrer-Policy mist.')

            # Strict-Transport-Security
            # max-age=31536000 of includeSubdomains
            try:
                strict_transport_security = resp.headers['Strict-Transport-Security']
                # print(strict_transport_security)
                if 'max-age=31536000'  and 'includeSubdomains' in strict_transport_security:
                    print('[*] Strict-Transport voldoet aan de eisen van NOREA, en heeft de headers max-age=31536000 en includeSubdomains juist ingesteld. ')
            except:
                print('[!] Strict-Transport-Security mist.')

            # X-Frame-Options
            # deny of sameorigin, één van beiden
            try:
                x_frame_options = resp.headers['X-Frame-Options']
                # print(x_frame_options)
                if 'deny' or 'sameorigin' in x_frame_options:
                    print('[*] X-Frame-Options voldoet aan de eisen van NOREA, en maakt gebruik van deny of sameorigin.')
            except:
                print('[!] X-Frame-Options mist.')
            print('------------')

            # controleren op verschillende requestmethodes & mogelijk onnodige data binnen de response header
            reqmethods = ['GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'OPTIONS', 'TRACE', 'CONNECT', 'TEST']
            headers = ['Server', 'Date', 'Via', 'X-Powered-By', 'X-Country-Code']

            print('\nControleren op onnodige request methodes:')
            print('-----')
            for method in reqmethods:
                resp = requests.request(method, url)
                if resp.status_code == 200:
                    print('[*] Ophalen van response header met request method', method, 'is mogelijk.')
            print('------------\n')
            
            # print('Controleren op mogelijk overbodige headers:')
            # print('-----')
            # for header in headers:
            #     try:
            #         result = resp.headers[header]
            #         print(header, result)
            #         if header != None:
            #             print('[i] %s: %s' % (header, result))
            #         else:
            #             print('[i] Geen mogelijk overbodige headers gevonden.')
            #     except Exception as e:
            #         return False
            # print('------------')

        else:
            print('[!] HTTP header niet kunnen ophalen.')


    except requests.exceptions.SSLError as g:
        print('[!] Website maakt gebruik van een ongeldig SSL certificaat, waardoor de response header niet opgehaald kon worden.')

# header_checker('https://vulnerable-website.com')
# header_checker('https://www.python.org')
# header_checker('https://github.com/')
# header_checker('https://www.martiniziekenhuis.nl')
# header_checker('https://expired.badssl.com/')
from email.policy import strict
import requests

def headerChecker(url):
# response header aanvragen
    resp = requests.get(url)
    if resp.status_code == 200:
        print('Response header opgehaald van', url, '\n')
        print('---')
        print('Rapportage:\n')

        # X-Content-Type-Options
        # nosniff 
        try:
            x_content_type = resp.headers['X-Content-Type-Options']
            if 'nosniff' in x_content_type:
                print('X-Content-Type-Options staan juist ingesteld volgens de aanbevolen waarden van NOREA.')
            else:
                print('X-Content-Type-Options voldoet niet aan de eisen van NOREA, ', x_content_type)
        except:
            print('X-Content-Type-Options staan niet ingesteld.')

        # Content-Security-Policy
        # unsafe-eval/unsafe-inline + nonce = goed
        # géén unsafe-eval/unsafe-inline = goed
        # unsafe-eval = fout
        try:
            content_security = resp.headers['Content-Security-Policy']
            # print(content_security)
            if (('unsafe-eval' or 'unsafe-inline' in content_security) and ('nonce' in content_security)):
                print('Content-Security-Policy maakt gebruik van unsafe-eval of unsafe-inline met een nonce.')
            elif 'unsafe-eval' or 'unsafe-inline' not in content_security:
                print('Content-Security-Policy maakt geen gebruik van unsafe-eval of unsafe-inline.')
            else:
                print('Content-Security-Policy voldoet niet aan de eisen van NOREA.')
        except:
            print('Content-Security-Policy staat niet ingesteld.')

        # Referrer-Policy
        # same-origin of no-referrer
        try:
            referrer_policy = resp.headers['Referrer-Policy']
            # print(referrer_policy)
            if 'same-origin' and 'no-referrer' in referrer_policy:
                print('Referrer-Policy maakt gebruik van same-origin én no-referrer.')
            elif 'same-origin' in referrer_policy:
                print('Referrer-Policy maakt gebruik van same-origin.')
            else:
                print('Referrer-Policy maakt geen gebruik van same-origin en staat niet ingesteld volgens de aanbevolen waarden van NOREA.')
        except:
            print('Referrer-Policy staat niet ingesteld.')

        # Strict-Transport-Security
        # max-age=31536000 of includeSubdomains
        try:
            strict_transport_security = resp.headers['Strict-Transport-Security']
            # print(strict_transport_security)
            if 'max-age=31536000'  and 'includeSubdomains' in strict_transport_security:
                print('Strict-Transport voldoet aan de eisen van NOREA, en heeft max-age=31536000 en includeSubdomains ingesteld.')
        except:
            print('Strict-Transport-Security staat niet ingesteld.')

        # X-Frame-Options
        # deny of sameorigin, één van beiden
        try:
            x_frame_options = resp.headers['X-Frame-Options']
            # print(x_frame_options)
            if 'deny' or 'sameorigin' in x_frame_options:
                print('X-Frame-Options voldoet aan de eisen van NOREA, en maakt gebruik van deny of sameorigin.')
        except:
            print('X-Frame-Options staat niet ingesteld.')
        print('------------')
    
    else:
        print('HTTP header niet kunnen ophalen. Klopt de URL?')

# headerChecker('https://vulnerable-website.com')
# headerChecker('https://www.python.org')
headerChecker('https://github.com/')
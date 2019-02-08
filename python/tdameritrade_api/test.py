from constants import *
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
import requests
import ssl
import os

import pdb

class Handler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        #Get the Auth Code
        path, _, query_string = self.path.partition('?')
        
        if len(query_string) > 0:
            code = parse_qs(query_string)['code'][0]

            #Post Access Token Request
            #headers = { 'Content-Type': 'application/x-www-form-urlencoded' }
            #data = { 'grant_type': 'authorization_code', 'access_type': 'offline', 'code': code, 'client_id': 'VALINVEST@AMER.OAUTHAP', 'redirect_uri': 'https://127.0.0.1:8080'}
            #authReply = requests.post('https://api.tdameritrade.com/v1/oauth2/token', headers=headers, data=data)
            
            #returned just to test that it's working
            self.wfile.write(authReply.text.encode())

httpd = HTTPServer(('127.0.0.1', 8080), Handler)

#SSL cert
httpd.socket = ssl.wrap_socket (httpd.socket, 
        keyfile=os.path.abspath('../auth/key.pem'), 
        certfile='../auth/certificate.pem', server_side=True)

r = requests.post(inst_url, data={'apikey':cid, 'symbol':'ATVI', 'projection':'fundamental&_1543891816302'})
r = requests.post(inst_url, data={'apikey':cid, 'symbol':'ATVI', 'projection':'fundamental&_1543891816302'})
pdb.set_trace()
httpd.serve_forever()

#90XJgpvTcgdcD7dyB/60kAGeJMckVY6D3VI839PI/ydofs6i1q9cd1i0sW6w74OIRbAtnYDVst8ThktsMOU5Z8CKMohdD1Ci5tk+dTqhvHaR9WPAwt+n75UESnBV5XK+h8McfSA/yWj2U8aUWm7SiF6C301MZHFIToOZUKnnJchnPDbkg32u+aBZKL4vMDeoT7kCtqEAp4uG7/wHTf/7zfdzl+LEI9LEFsZhDR4AQgSUTkEqcbEC05IzBFX6GMBmLhNIM13k9vhatc2wecLIVHVYu4uqxl0zSk7MmGkNdRAT56qOjFETkJC5vMxuHEjUIYwxxQcXbysyISakzmNE2T5lcZ3KrvEH/VaWgvl0OIXFKa26xrWerArhACibOcXwE+NcCM2d+1cD/l8gXPxWGbtw+QT2gd602DztwcNcypoe9OesCLb3X2xNyhS100MQuG4LYrgoVi/JHHvlZBVC+orA6hU4mwyeau1a5w9+fhkEHM769pJDVqH7P21LUkeqnI9Xm97NOZFGQ87tcGDzvTXq35PxlPrEa12ofKwwMxEOV7oi6nKIW7a29v8kCIi+vzFrUo4p6xFHHC4K6WJ4E3ezCcoL2d+L2AK1aHCJfC0TfqCr/HGRVVDVEo1BF+BTnlVrulSlLwl+uudN1SoCTimihIG1+cqDq4NgmqkJs2lBI0K2kFhVrVU83YNlcXCHXZ91fPJNUgIecF30BIiVSMJR4wVjUKIJUxiSyXuGQLNoZk/VR8pjts9T+VHEuj4f4newqxp8TKntCAy2pPxo39Fyi6nNtV48opwsmWfKKYLa4ZglY83yXBr3CGAO1HUUx3glHCn9XPE92fvFrhy/x1mswbKp3GCSub4GT0qn69xX/9rY8WSU5aHyUQf0IhmodrqqzyMRkTQ=212FD3x19z9sWBHDJACbC00B75E

#Access-Control-Allow-Headers:
#origin
#Access-Control-Allow-Methods:
#GET
#Access-Control-Allow-Origin:
#https://developer.tdameritrade.com
#Access-Control-Max-Age:
#3628800
#Cache-Control:
#no-cache
#Connection:
#keep-alive
#Content-Length:
#2137
#Content-Type:
#application/json;charset=UTF-8
#Date:
#Mon, 03 Dec 2018 23:54:32 GMT
#Strict-Transport-Security:
#max-age=31536000
#X-Application-Context:
#OAUTH_SERVICE:run:8080
#{
#  "access_token": "qk1y20zYAVfHg82MQyzusWtIvIv/35x2KxomHyGYFN4hv6K1g0HSmLsqPyJAIWmY70Zy1iTQ2kt3Yz3L+Ke67EEhXEicIO5MVo52AoewdfpEWhErwooKUatPu9sBalwYITe1BbWDKIU0oqni/oviuQ+GK9wY1igom43+TMzCEW/64BavjQhE3D8dTRfAu9NncLirOCZMBA5e4yFPpfKT493CLBUskjVZlIIRBqDKd9ZRICGCv6HtKW9yYEK2tg6Q2bp2ByEtl8dC6yrBUg3SM264PGMS6BnaRfuLLg5uDRsGgyCsKke4kcKrLkr6jtPLeduivkLufLtyxUL8KtJfw5bOeKwLLWQGgnIAyHKJWiOLdU4rDUuMV46JSoXQRm6DzNb+n6WEd1WkeKhVIjtlHUwQpVZ2TNkwf59OGcS4GPHS8zaGJprFiGfSHPu8fJa7rZIn7AQczzyGAXqzrjyJPC9jH15Ui5OuOvZI/7IVj1Hxi4JQlLgzBk8Z1E7100MQuG4LYrgoVi/JHHvllK7HleVEuwlqf0fCP9cUnF1Pap7S8CmG7ClGX64s2tck/J894YdcbtAT+pSGBHX1yCQObxkNdONxY3ZZZkd5V846WMNe7pZ9HwAaUjm05V899fWY0A8eXGIs9kLdn6ChOOHFMICQshuCiwya7wfA/YTuCSqHEFsEBWwXdNFaQAlDjalaF4kepByMoFu6djldarN6J9bgjXZZK/dLEKjNmmumHtj7ETja5Ffqf6ptx/FAyYRdKZH0rcqPTU4pz5OFpKfTBRcV1ByzI2cNLO8aZHwL33YjOjgcPwOHQKcVq3/FjwAWb2Og7hGfWhYKM7kHUKMUikEJd3h8yQUDhK1NLmlDhZ1Gt7d7c7HKcnEQFqcYUSnfxvmEt6/zzFcGdlufTCLPpFJxkG0MkInf4TtZLTwsIxYOuoBslA1e4Z5wMN15AjK4bDfHRboquG5wCwHFgm6XMuBumGYqVX1+/9DJMoKhNbsqJrR0XwV8vEWbaAQrbaIgeIj4VJ+IYwY=212FD3x19z9sWBHDJACbC00B75E",
#  "refresh_token": "ClbY2UfzIXXA8EQoFm84dhpdbT2lHJjkH2t1KuPr2+CoGQWP4S/yp2QI/h8uIrKI4sQe9rgnXbnAJNByQbq4NHbrQp7we8WwzpGZh7jw6lnV9v9AHFQhCsMC+XIy8xrnssVbTSmnF56zmUon/gaqJFJRumePsxIpD6NUzZK845RIdnsDn7XweGge9xcr1jkQyEkTcNz/c9TIs4zyM4NfGFhLQBV2AJfEgPsSLPioQLbetYiLFp013FkrsCogG5Oxhzs8DkioYAqHvzuI0IMXI8St22zdG6F9xRWtH2qNQ3Kwj8uEqhJ5FrPLhVUXNKgFE8Kal4U9MpOZw5/R+KATQLl+QI92BTlkMd+ISU9GK+IVwJnEXcqBKWkzWNbU+tXIFFJ7W10iiASPzEnY7jUVsgaVYcYkn7s8OSxUXFMiwIl8og9ccq40R85NTrD100MQuG4LYrgoVi/JHHvlQpem7pPD68l0LZK70i+skyQbqcKQ9Zwd3YXiRLB70zFDTQL6Mi64tLejeBPDXHkr61YsVEeCQJtzyIE2vblQ0OLgwW7XUjVFO0r5RQB4ZwYmYmlZO5YDB2L8SByNoBwsl0k/eBf1xhJC4Pr2lkXT1bGmNtJtkhgEBXMqkYUOaRGycpfb9KrRfDpsc8yFLYYAN0gkgqLvtY+em6pPS793wspxnYuM2dTc4n9UbOQ7iOQljEPn4zp6Z8/5F6deg3YR6Q1ycBIQv6t8zdfuoDbc+MdfQ70qnJizrxgQYkMx0PMuHuRLX6cchsqcUVKPZTd3oOOLU3+HCFa1bhqnIouHKpFbm8XKRyI+luWF5QrxO1ZjOy2O4/v+NPFVN/kQ/7nw5VLJMHDl7EsFwkK7yyDu0kaJqUrOplLJWJJhQKBa4em1wRJe5oJOMiRzHCc=212FD3x19z9sWBHDJACbC00B75E",
#  "expires_in": 1800,
#  "refresh_token_expires_in": 7776000,
#  "token_type": "Bearer"
#}
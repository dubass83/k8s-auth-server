""" Constants file for Auth0's seed project
"""
ACCESS_TOKEN_KEY = 'access_token'
API_ID = 'API_ID'
APP_JSON_KEY = 'application/json'
AUTH0_CLIENT_ID = 'AUTH0_CLIENT_ID'
AUTH0_CLIENT_SECRET = 'AUTH0_CLIENT_SECRET'
AUTH0_CALLBACK_URL = 'AUTH0_CALLBACK_URL'
AUTH0_DOMAIN = 'AUTH0_DOMAIN'
AUTH0_AUDIENCE = 'AUTH0_AUDIENCE'
AUTHORIZATION_CODE_KEY = 'authorization_code'
CLIENT_ID_KEY = 'client_id'
CLIENT_SECRET_KEY = 'client_secret'
CODE_KEY = 'code'
CONTENT_TYPE_KEY = 'content-type'
GRANT_TYPE_KEY = 'grant_type'
PROFILE_KEY = 'profile'
REDIRECT_URI_KEY = 'redirect_uri'
SECRET_KEY = 'ThisIsTheSecretKey'
JWT_PAYLOAD = 'jwt_payload'
ID_TOKEN = 'ID_TOKEN'
APP_HOST = 'APP_HOST'
KUBERNETES_UI_HOST = 'KUBERNETES_UI_HOST'
AUTH0_CONNECTION = 'AUTH0_CONNECTION'
# For test amazon CA
K8S_CA = """
-----BEGIN CERTIFICATE-----
MIIDQTCCAimgAwIBAgITBmyfz5m/jAo54vB4ikPmljZbyjANBgkqhkiG9w0BAQsF
ADA5MQswCQYDVQQGEwJVUzEPMA0GA1UEChMGQW1hem9uMRkwFwYDVQQDExBBbWF6
b24gUm9vdCBDQSAxMB4XDTE1MDUyNjAwMDAwMFoXDTM4MDExNzAwMDAwMFowOTEL
MAkGA1UEBhMCVVMxDzANBgNVBAoTBkFtYXpvbjEZMBcGA1UEAxMQQW1hem9uIFJv
b3QgQ0EgMTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALJ4gHHKeNXj
ca9HgFB0fW7Y14h29Jlo91ghYPl0hAEvrAIthtOgQ3pOsqTQNroBvo3bSMgHFzZM
9O6II8c+6zf1tRn4SWiw3te5djgdYZ6k/oI2peVKVuRF4fn9tBb6dNqcmzU5L/qw
IFAGbHrQgLKm+a/sRxmPUDgH3KKHOVj4utWp+UhnMJbulHheb4mjUcAwhmahRWa6
VOujw5H5SNz/0egwLX0tdHA114gk957EWW67c4cX8jJGKLhD+rcdqsq08p8kDi1L
93FcXmn/6pUCyziKrlA4b9v7LWIbxcceVOF34GfID5yHI9Y/QCB/IIDEgEw+OyQm
jgSubJrIqg0CAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAOBgNVHQ8BAf8EBAMC
AYYwHQYDVR0OBBYEFIQYzIU07LwMlJQuCFmcx7IQTgoIMA0GCSqGSIb3DQEBCwUA
A4IBAQCY8jdaQZChGsV2USggNiMOruYou6r4lK5IpDB/G/wkjUu0yKGX9rbxenDI
U5PMCCjjmCXPI6T53iHTfIUJrU6adTrCC2qJeHZERxhlbI1Bjjt/msv0tadQ1wUs
N+gDS63pYaACbvXy8MWy7Vu33PqUXHeeE6V/Uq2V8viTO96LXFvKWlJbYK8U90vv
o/ufQJVtMVT8QtPHRh8jrdkPSHCa2XV4cdFyQzR1bldZwgJcJmApzyMZFo6IQ6XU
5MsI+yMRQ+hDKXJioaldXgjUkK642M4UwtBV8ob2xJNDd2ZhwLnoQdeXeGADbkpy
rqXRfboQnoZsG4q5WTP468SQvvG5
-----END CERTIFICATE-----
"""
LOGO_URL = 'LOGO_URL'
CLI_AUTH = """
#!/usr/bin/python3

from os import environ as env
from dotenv import load_dotenv, find_dotenv
from jose import jwt
from six.moves.urllib.request import urlopen
from os.path import expanduser

import getpass
import requests
import json
import sys

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_CLIENT_ID = env.get('AUTH0_CLIENT_ID')
AUTH0_DOMAIN = env.get('AUTH0_DOMAIN')
APP_HOST = env.get('APP_HOST')
HOME = expanduser("~")

def auth():
  sys.stderr.write("Login: ") 
  login = input() 
  password = getpass.getpass()

  r = requests.get("http://"+APP_HOST+"/kubectl?username="+login+"&password="+password)

  resp = json.loads(r.text)

  if 'error' in resp:

    print("There was an auth0 error: "+resp['error']+": "+resp['error_description'])

  else:

    id_token = resp['id_token']

    jwks = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")

    with open(HOME+'/.kube/jwks.json', 'w') as f: f.write (jwks.read().decode('utf-8'))
    with open(HOME+'/.kube/id_token', 'w') as f: f.write (id_token)

    print(id_token) 

def main():
  try:
    with open(HOME+'/.kube/jwks.json', 'r') as content_file: jwks = content_file.read()
    with open(HOME+'/.kube/id_token', 'r') as content_file: id_token = content_file.read()

    payload = jwt.decode(id_token, jwks, algorithms=['RS256'],
                       audience=AUTH0_CLIENT_ID, issuer="https://"+AUTH0_DOMAIN+"/")
    
    print(id_token) 
  except OSError as e:
    auth()
  except jwt.ExpiredSignatureError as e:
    auth()
  except jwt.JWTClaimsError as e:
    auth()


if __name__ == '__main__':
  main()
"""
CLI_REQUIREMENTS = """
python-dotenv
requests
python-jose
"""
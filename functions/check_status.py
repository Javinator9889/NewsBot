import urllib.request as rq
import requests

request = requests.get('http://altadensidad.com/%3Fp%3D98195')
print(request.status_code)

#print(rq.urlopen("http://altadensidad.com/%3Fp%3D98195").getcode())

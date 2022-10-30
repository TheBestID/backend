import time

import requests as requests

start = time.time()
r = requests.post('http://localhost:8000/user/address',
                  json={'address': '134'})
print(r.text, time.time() - start)

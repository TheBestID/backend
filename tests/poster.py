# import aiohttp
import asyncio
import json
import time

import aiohttp as aiohttp
import requests
from quart_jwt_extended import create_access_token

# def get(url):
#     return requests.post('http://localhost:5000/registration',
#                          json={'s_name': fake.last_name(), 'f_name': fake.first_name(),
#                                'phone': fake.phone_number()[:12],
#                                'email': fake.free_email(), 'birthday': fake.date(),
#                                'password1': '1234',
#                                'password2': '321'}).text

#
# async def fetch(session, url):
#     async with session.get(url,
#                            json={'uid': '50e70229-dc29-43d3-a271-45a6c1226161'}) as response:
#         return await response.text()


#
# #
# async def main():
#     urls = ['http://localhost:8000/user/profile/personalv2'] * 500
#     tasks = []
#     async with aiohttp.ClientSession() as session:
#         for url in urls:
#             tasks.append(fetch(session, url))
#         start = time.time()
#         htmls = await asyncio.gather(*tasks)
#         print(time.time() - start)
#         print(htmls)


# v1: 39.65526056289673
# v2: 40.362417459487915
# v1: 28.747196912765503  39.50178241729736
# v2: 27.86713933944702


# asyncio.run(main())
# r = requests.get('http://localhost:5000/admin')

# start = time.time()
# r = requests.post('http://localhost:5000/user/registration',
#                   json={'s_name': fake.last_name(), 'f_name': fake.first_name(), 'phone': fake.phone_number()[:12],
#                         'email': fake.free_email(), 'birthday': fake.date(), 'mailing': True,
#                         'password1': '1234',
#                         'password2': '1234'})
# print(r.text, time.time() - start)

# start = time.time()
# r = requests.post('http://localhost:5000/user/login',
#                   json={'login': 'jking@yahoo.com', 'password': '1234'})
# print(r.text, time.time() - start)
#
# start = time.time()
# r = requests.get('http://localhost:5000/user/profile/estimates',
#                  json={'user_id': '50e70229-dc29-43d3-a271-45a6c1226164'})
# print(r.text, time.time() - start)

# start = time.time()
# r = requests.post('http://localhost:5000/')
# headers={
#     'Authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NjE4NzA0OTIsIm5iZiI6MTY2MTg3MDQ5MiwianRpIjoiYWJhZTQwOGUtMzM1Mi00MjQ1LWIyMDItM2E1ZTc1MjA0YjQwIiwiZXhwIjoxNjYxODcxMzkyLCJpZGVudGl0eSI6IjUwZTcwMjI5LWRjMjktNDNkMy1hMjcxLTQ1YTZjMTIyNjE2NCIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyIsInVzZXJfY2xhaW1zIjp7ImFnZSI6MTIxfX0.pUSVb2VtL6SrRBf23wLGnOs4752D6savBkbgVkHtaT8"})
# print(r.text, time.time() - start)

#
# start = time.time()
# r = requests.get('http://localhost:5000/user/profile/locations',
#                  json={'user_id': '50e70229-dc29-43d3-a271-45a6c1226164'})
# print(r.text, time.time() - start)

# start = time.time()
# r = requests.post('http://localhost:5000/user/profile/locations',
#                   json={'user_id': '50e70229-dc29-43d3-a271-45a6c1226164',
#                         'title': fake.name(),
#                         'city': fake.name(),
#                         'street': fake.name(),
#                         'flat': '43',
#                         'index': '123456',
#                         'house': fake.first_name(),
#                         'method': 'hi'
#                         })
# print(r.text, time.time() - start)


# data = {'title': 'tort'}
# r = requests.post('http://localhost:5000/admin/banners', data=data, files=files)
# print(r.text)

# start = time.time()
# r = requests.put('http://localhost:1000/user/profile',
#                  json={'uid': '0748120f-870a-40e9-a0a6-5daf15fa6fea', 'field': 'info', 's_name': fake.last_name(),
#                        'f_name': fake.first_name(), 'phone': fake.phone_number()[:12],
#                        'email': fake.free_email(), 'birthday': fake.date()})
# print(r.text, time.time() - start)


# start = time.time()
# r = requests.delete('http://localhost:1000/user/profile',
#                     json={'uid': '0748120f-870a-40e9-a0a6-5daf15fa6fea'})
# print(r.text, time.time() - start)

# start = time.time()
# r = requests.put('http://localhost:1000/user/profile',
#                  json={'uid': '0748120f-870a-40e9-a0a6-5daf15fa6fea', 'field': 'password',
#                        'new_password1': '1234', 'new_password2': '1234', 'old_password': '123', })
# print(r.text, time.time() - start)

# start = time.time()
# r = requests.post('http://localhost:1000/user/review',
#                   json={'uid': '56902f5c-bc86-4b91-99cf-3ab67191978f',
#                         'pid': '81f241d0-313b-4ee9-8312-69b36c912810',
#                         'description': fake.name(),
#                         'stars': 4})
# print(r.text, time.time() - start)
#
# start = time.time()
# r = requests.post('http://localhost:1000/user/address',
#                   json={'uid': '56902f5c-bc86-4b91-99cf-3ab67191978f',
#                         'title': fake.name(),
#                         'city': fake.name(),
#                         'street': fake.name(),
#                         'flat': '43',
#                         'index': '123456',
#                         'house': fake.first_name(),
#                         'method': 'hi'})
# print(r.text, time.time() - start)

# start = time.time()
# r = requests.delete('http://localhost:1000/user/address',
#                     json={'uid': '56902f5c-bc86-4b91-99cf-3ab67191978f',
#                           'aid': 'd389268a-356c-479a-9fdd-b20c4f0e5190'})
# print(r.text, time.time() - start)
# #
# start = time.time()
# r = requests.put('http://localhost:1000/user/address',
#                  json={'uid': '56902f5c-bc86-4b91-99cf-3ab67191978f',
#                        'aid': 'da2975a2-6e66-48a1-af7f-64611cf8ed76',
#                        'title': fake.name(),
#                        'city': fake.name(),
#                        'street': fake.name(),
#                        'flat': '43',
#                        'index': '123456',
#                        'house': fake.first_name(),
#                        'method': 'hi'})
# print(r.text, time.time() - start)

# start = time.time()
# r = requests.post('http://localhost:1000/user/order',
#                   json={'uid': '56902f5c-bc86-4b91-99cf-3ab67191978f',
#                         'aid': 'da2975a2-6e66-48a1-af7f-64611cf8ed76',
#                         'delivery_description': fake.name(),
#                         'receipt': fake.name(),
#                         'items': [
#                             {'item_id': '02849a89-ef52-47e0-8459-9877565f248b',
#                              'quantity': 3,
#                              'purchase_price': 1200},
#                             {'item_id': '0fc61574-a332-41ab-9167-b81397d27438',
#                              'quantity': 3,
#                              'purchase_price': 1200}
#                         ]})
# print(r.text, time.time() - start)

# print(r.text, time.time() - start)
# ava = open('static/img/0b843445072b407ab481ffb93427dfef.jpg', 'rb')
# d = {'title': fake.company(), 'f_name': fake.first_name(), 's_name': fake.last_name(),
#      'phone': fake.phone_number()[:12],
#      'email': fake.free_email(), 'tg': fake.free_email(), 'birthday': fake.date(), 'end_work': fake.date(),
#      'password1': '1234',
#      'password2': '1234'}
# start = time.time()
# r = requests.post('http://localhost:1000/supplier/registration',
#                   files={
#                       'avatar': ('0b843445072b407ab481ffb93427dfef.jpg', ava, 'application/octet-stream'),
#                       'contract': ('', con, 'application/octet-stream'),
#                       'json': (None, json.dumps(d), 'application/json')
#                   })
# print(r.text, time.time() - start)
# sid = r.json()['supplier_id']

# start = time.time()
# r = requests.post('http://localhost:1000/supplier/orders',
#                   json={'sid': 'dd22d040-b1f0-4bec-9f97-4efad719a091'})
# print(r.text, time.time() - start)
# #
# start = time.time()

# ava.close()
# con.close()

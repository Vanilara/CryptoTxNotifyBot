import requests


res = requests.get('https://apilist.tronscanapi.com/api/account/wallet?address=TSTR3hN7sowCkAHDpYQ62rrFR8A4ctwFr3&asset_type=0', headers={'accept': 'application/json', 'TRON-PRO-API-KEY': 'dd4b5a9f-6796-4f07-b67e-2c4418738c19'})
print(res)
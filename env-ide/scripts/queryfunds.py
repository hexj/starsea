import requests
r = requests.get('http://fund.eastmoney.com/js/fundcode_search.js')
print(r.text)
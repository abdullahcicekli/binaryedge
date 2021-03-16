import time
import json
import requests

headers = {
    'authority': 'api.binaryedge.io',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'accept': 'application/json, text/plain, */*',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'content-type': 'application/json;charset=UTF-8',
    'origin': 'https://app.binaryedge.io',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://app.binaryedge.io/',
    'accept-language': 'en-US,en;q=0.9',
}

data = '{"email":"example@example.com","password":"examplepassword"}' #Platform Giriş Bilgileri Buraya Girilecek.

token = requests.post('https://api.binaryedge.io/v2/user/login/', headers=headers, data=data)
print()
headers = {
    'authorization': f"JWT {token.json()['token']}"
}
be_list = []
for i in range(1, 10): #KAÇ SAYFA ÇEKİLECEK SE BURADA BELİRTİLECEK.
    time.sleep(1)
    response_main = requests.get(
        f"https://api.binaryedge.io/v2/query/web/search?page={i + 1}&query=port:9200%20type:elasticsearch",
        headers=headers)
    # print(response_main.json())
    # print("\n")
    docs = response_main.json()
    for ind in range(len(docs['events'])):
        new_dict = {}
        if "geoip" in docs['events'][ind].keys():
            new_dict['country_name'] = docs['events'][ind]['geoip']['country_name']
        if "ip" in docs['events'][ind].keys():
            new_dict['ip'] = docs['events'][ind]['ip']
        if "created_at" in docs['events'][ind].keys():
            new_dict['created_at'] = docs['events'][ind]['created_at']
        if "ostype" in docs['events'][ind].keys():
            new_dict['ostype'] = docs['events'][ind]['ostype']
        if "protocol" in docs['events'][ind].keys():
            new_dict['protocol'] = docs['events'][ind]['protocol']
        if "elasticsearch" in docs['events'][ind].keys():
            if "jvm" in docs['events'][ind]['elasticsearch']:
                new_dict['docs'] = docs['events'][ind]['elasticsearch']['jvm']
            if "docs" in docs['events'][ind]['elasticsearch']:
                new_dict['docs'] = docs['events'][ind]['elasticsearch']['docs']


        be_list.append(new_dict)


with open("elasticleaked.json","w") as f:
    json.dump(be_list, f, indent=3)

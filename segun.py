import requests
import json

urlbase = 'https://zenkit.com/api/v1/'
cabecera = {'Content-Type': 'application/json',
            'Zenkit-API-Key': 'jffaf7ne-X1ELSpJZLdRlE5uAWIbWC47rJlna51h2'}


def get_account_info():
    url = urlbase + "auth/currentuser"
    response = requests.get(url, headers=cabecera)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

def get_ws():
    url = urlbase + "users/me/workspacesWithLists"
    response = requests.get(url, headers=cabecera)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None



account_info = get_account_info()
ws = get_ws()

if account_info is not None:
    print("En linea: ")
    #for k, v in account_info.items():
    #    print('{0}:{1}'.format(k, v))
else:
    print('[!] Error')
    exit

if ws is not None:
    for k, v in ws[1].items():
        print('{0}:{1}'.format(k, v))
    #print (ws)
else:
    print('[!] Error')
    exit()


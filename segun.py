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

def jsonAFichero(df):
    fichero = "/tmp/prueba.json"

    with open(fichero, 'w') as file:
        json.dump(df, file)
        file.close()

def put_cambioElemento(listId, listEntryId, elementId, elementChange):
    url = urlbase + "/api/v1/lists/" + listId + "/entries/" + listEntryId + "/elements/" + elementId
    response = requests.put(url, headers=cabecera, params=elementChange)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

###################################################
#### Inicio del programa
###################################################


account_info = get_account_info()
ws = get_ws()
jsonAFichero(ws)

if account_info is not None:
    print("En linea: ")
    # for k, v in account_info.items():
    #    print('{0}:{1}'.format(k, v))
else:
    print('[!] Error1')
    exit

if ws is not None:
    for k, v in ws[0]["lists"][0]["settings"]["calendarSync"].items():
        print('{0}:{1}'.format(k, v))

else:
    print('[!] Error2')
    exit()

print(ws[0]["lists"][0]["settings"]["calendarSync"]["calendarName"])

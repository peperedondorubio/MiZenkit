import requests
import json
import sys

version = "1.0"
urlbase = 'https://zenkit.com/api/v1/'
cabecera = {'Content-Type': 'application/json',
            'Zenkit-API-Key': 'jffaf7ne-X1ELSpJZLdRlE5uAWIbWC47rJlna51h2'}

def crearTareaMiLista(listShortId,textoTarea):
    url = urlbase + "lists/" + listShortId + "/entries"

    payload = '{   \
    "sortOrder": "highest",   \
    "7fba08c0-5c02-4c73-a373-8609ffb2aea5_text": '
    payload += '"' + textoTarea + '",  \
    "2c4f48c2-1567-4991-8289-9552d5a2b81f_categories": "1190201"  \
    }'

    response = requests.post(url, data=payload, headers=cabecera)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

###############################################################################

listShortId = "H1bSOMA9f"  # Lista de Mis Cosas

if len(sys.argv) > 1:
    jsonTarea = crearTareaMiLista(listShortId, sys.argv[1])
    if jsonTarea is None:
        print('Error en la creación: ', jsonTarea)
        exit(1)
else:
    exit(2)

exit (0)

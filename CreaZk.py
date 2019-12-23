import requests
import json
import sys

version = "1.0"
urlbase = 'https://zenkit.com/api/v1/'
cabecera = {'Content-Type': 'application/json',
            'Zenkit-API-Key': 'jffaf7ne-X1ELSpJZLdRlE5uAWIbWC47rJlna51h2'}
listShortId = "H1bSOMA9f"  # Lista de Mis Cosas
estadoHoy = "1190201"  # Estado Hoy
uuidEstadoHoy = "2c4f48c2-1567-4991-8289-9552d5a2b81f_categories"  # uuid Estado Hoy
uuidVencimiento = "98029764-6bbe-485d-b4b1-1c4d80809446_date"  # uuid vencimiento
nuevoTemita = "7fba08c0-5c02-4c73-a373-8609ffb2aea5_text" # uuid Texto de la tarea


def crearTareaMiLista(listShortId, argumentos):
    url = urlbase + "lists/" + listShortId + "/entries"

    if len(argumentos) == 1:
        return None   # Sin argumentos

    vencimiento=""
    textoTarea=argumentos[1]

    payload = '{  "sortOrder": "lowest",  "'
    payload += nuevoTemita + '": '
    payload += '"' + textoTarea + '",  "'
    payload += uuidEstadoHoy + '": "' + estadoHoy + '"'
    payloadFin = ' }'

    if len(argumentos) == 2:
        payload += payloadFin
    if len(argumentos) == 3:
        vencimiento=argumentos[2]
        payloadVencimiento = ', "' + uuidVencimiento + '": "' + vencimiento + '"'
        payload += payloadVencimiento + payloadFin
    if len(argumentos) > 3:
        return None

    response = requests.post(url, data=payload, headers=cabecera)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        print(payload)
        return None

###############################################################################

jsonTarea = crearTareaMiLista(listShortId, sys.argv)
if jsonTarea is None:
    print('Error en la creación: ', jsonTarea)
    exit(1)

exit(0)       #  Está bien


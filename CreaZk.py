import requests
import json
import sys

# Estáticas
version = "1.2"
urlbase = 'https://zenkit.com/api/v1/'
cabecera = {'Content-Type': 'application/json',
            'Zenkit-API-Key': 'jffaf7ne-X1ELSpJZLdRlE5uAWIbWC47rJlna51h2'}

# Estáticas de "Mis Cosas"
listShortId = "H1bSOMA9f"  # Lista de Mis Cosas
estadoHoy = "1190201"  # Estado Hoy
uuidEstadoHoy = "2c4f48c2-1567-4991-8289-9552d5a2b81f_categories"  # uuid Estado Hoy
uuidVencimiento = "98029764-6bbe-485d-b4b1-1c4d80809446_date"  # uuid vencimiento
nuevoTemita = "7fba08c0-5c02-4c73-a373-8609ffb2aea5_text" # uuid Texto de la tarea


def crearTareaMiLista(listShortId, argumentos, nuevoTemita, uuidEstadoHoy, estadoHoy, uuidVencimiento):

    url = urlbase + "lists/" + listShortId + "/entries"
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

# No tenemos parámetros
if len(sys.argv) == 1:
    print('Error en la creación: ', jsonTarea)
    exit(1)

# Crea nueva tarea
jsonTarea = crearTareaMiLista(listShortId, sys.argv, nuevoTemita, uuidEstadoHoy, estadoHoy, uuidVencimiento)

exit(0)       # Está todo bien


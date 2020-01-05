import requests
import json
import argparse
import sys
from datetime import datetime, date, timedelta

version = "1.1"
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


def putCambioEstado(listId, listEntryId, elementId, uuidElementId, nuevoValor):
    url = urlbase + "lists/" + listId + "/entries/" + listEntryId + "/elements/" + elementId
    payload = '{\n\t    \"' + uuidElementId + '_categories\": \"' + nuevoValor + '\"\n}\n'

    response = requests.put(url, data=payload, headers=cabecera)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


def postFiltroPorFecha(listShortId, elementId, fecha, groupby):
    url = urlbase + "lists/" + listShortId + "/entries/filter/list"

    # Excluyo estados: hoy, hecho y cancelado (exclude)

    datos_post = '{ \
               "filter": {  \
                   "AND": {   \
                       "TERMS": [{  \
                           "elementId":'
    datos_post += elementId + ',   \
                           "modus": "contains",    \
                           "negated": false,      \
                           "dateType": 10,        \
                           "dateFrom": null,      \
                           "dateTo": "'
    datos_post += fecha + '"   \
                       }   \
                       ]   \
                   }},     \
               "groupByElementId": '
    datos_post += groupby + ',    \
               "exclude": [1190201,1190207,1190208],   \
               "allowDeprecated": false,       \
               "taskStyle": false,             \
               "skip": 0                      }'

    response = requests.post(url, data=datos_post, headers=cabecera)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

def argumentosEntrada():
    prev = 1
    verbose = bool(0)

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Más log", action="store_true")
    parser.add_argument("-p", "--previo", help="Dias previos para cambio de estado")
    args = parser.parse_args()

    if args.previo:
        prev = int(args.previo)

    if args.verbose:
        verbose = bool(1)

    return [prev, verbose]

###################################################
#### Inicio del programa
###################################################

# Valores estáticos
listShortId = "H1bSOMA9f"  # Lista de Mis Cosas
listId = "218913"  # Lista de Mis Cosas
elementId = "2260113"  # Identificador de Fecha de Vencimiento
EstadoId = "2260111"  # Agrupado por Estado Original
uuidEstado = "2c4f48c2-1567-4991-8289-9552d5a2b81f"  # UUid Del Estado Original
estadoHoy = "1190201"  # Estado por el que se cambia (Hoy)

# Lista de parametros de entrada. Devuelve numero de dias previos de cambio de estado (opción -p)
[previos, verbose] = argumentosEntrada()
if previos == 0:
    sys.stderr.write("Falla ArgumentosEntrada\n")
    exit(1)  # No debería pasar

# Calcula el día de mañana
hoy = date.today()  # Asigna fecha actual
mañana = hoy + timedelta(days=previos)
strMañana = str(mañana)
print("segun.py -->  Versión" + version)
print("Fecha: " + str(datetime.now()))

# Busco entradas con fecha anterior de mañana y que no esten Hecho o Cancelado o Archivado
jsonFiltro = postFiltroPorFecha(listShortId, elementId, strMañana, EstadoId)
if jsonFiltro is None:
    sys.stderr.write("Error en el filtro: \n" + jsonFiltro)
    exit(1)

# Itero por las entradas encontradas y cambio su estado a Hoy
elementos = int(jsonFiltro['countData']['filteredTotal'])
iterador = 0
while iterador < elementos:
    elementId = str(jsonFiltro["listEntries"][iterador]['id'])
    retPut = putCambioEstado(listId, elementId, EstadoId, uuidEstado, estadoHoy)
    if retPut is None:
        sys.stderr.write('Error en Cambio de estado: ' + elementId)
        exit(1)
    print("--> " + jsonFiltro["listEntries"][iterador]['displayString'])
    iterador += 1

print()  # Un espacio al final
exit(0)

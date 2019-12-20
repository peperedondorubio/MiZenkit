import requests
import json
from datetime import date, timedelta

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

    response = requests.put( url, data=payload, headers=cabecera)
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None

def postFiltroPorFecha(listShortId, elementId,fecha, groupby):

    url = urlbase + "lists/" + listShortId + "/entries/filter/list"

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
               "exclude": [1190207,1190208],   \
               "allowDeprecated": false,       \
               "taskStyle": false,             \
               "skip": 0                      }'

    response = requests.post(url, data =datos_post, headers=cabecera)

    print (datos_post)
    return json.loads(response.content.decode('utf-8'))

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None


###################################################
#### Inicio del programa
###################################################

# Valores estáticos
listShortId = "H1bSOMA9f"   # Lista de Mis Cosas
listId =  "218913"          # Lista de Mis Cosas
elementId = "2260113"        # Identificador de Fecha de Vencimiento
EstadoId = "2260111"        # Agrupado por Estado Original
uuidEstado = "2c4f48c2-1567-4991-8289-9552d5a2b81f"  # UUid Del Estado Original
estadoHoy = "1190201" # Estado por el que se cambia (Hoy)

hoy = date.today()  # Asigna fecha actual
mañana = hoy + timedelta(days=1)
strMañana = str(mañana)
print(mañana)  # "2019-12-20T12:00:00.000Z"

# Busco entradas con fecha anterior de mañana y que no esten Hecho o Cancelado o Archivado
jsonFiltro = postFiltroPorFecha(listShortId, elementId, strMañana, EstadoId)
if jsonFiltro is None:
    print('Error en Filtro')
    exit

#Itero por las entradas encontradas y cambio su estado a Hoy
elementos = int(jsonFiltro['countData']['filteredTotal'])
iterador = 0
while iterador < elementos:
    elementId = str(jsonFiltro["listEntries"][iterador]['id'])
    retPut = putCambioEstado(listId,elementId,EstadoId,uuidEstado,estadoHoy)
    if retPut is None:
        print('Error en Cambio de estado')
        exit
    iterador += 1

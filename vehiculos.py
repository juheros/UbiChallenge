import requests
import json
import time
from peewee import *

db = SqliteDatabase('rutas.db')

URL_API = 'http://things.ubidots.com/api/v1.6/'
TOKEN = 'vUOiTKHogWDlj7fjUgZLfG1KSA0WVuK941zLEHQg7LNkLeoQlwPwfJ5hgRNI'
VARIABLES_ID =  [
                    '52d9593bf91b28134f3b4d71',
                    '52d9595af91b28134f3b4d83',
                    '52d9596bf91b28135407f6b3',
                    '52d9597cf91b28135407f6d3',
                    '52d9598cf91b2813517c8d3a'
                ]

class Ruta(Model):
    """Modelo Ruta: mapeo de la tabla rutas a objetos (ORM) """
    ruta = CharField()
    latitud = CharField()
    longitud = CharField()

    class Meta:
        database = db


class Vehiculo:
    """Clase de los objetos vehiculo."""
    def __init__(self,variable_id=None, latitud=None, longitud=None,
                    gasolina=100, ruta=None):
        self._ruta = list(Ruta.select().where(Ruta.ruta == ruta))
        self._indice_ruta = 0
        self._variable_id = variable_id
        self._url = 'variables/'+ self._variable_id +'/values'
        self._latitud = latitud
        self._longitud = longitud
        self._gasolina = gasolina

    def conducir(self):
        self.set_ubicacion(self._ruta[self._indice_ruta].latitud, self._ruta[self._indice_ruta].longitud)
        self.set_gasolina(self._gasolina-1)

        if self._ruta[self._indice_ruta] == self._ruta[-1]:
            """
            Si completo la ruta, inicia el sprint nuevamente 
            y llena el tanque de gasolina
            """
            self._indice_ruta = 0
            self._llenar_tanque()

        else:
            self._indice_ruta += 1

    def reportar(self):
        headers = {'content-type': 'application/json', 'X-Auth-Token' : TOKEN}

        data = {'value': str(self._gasolina), 'context':'{"latitud":"'
                +str(self._latitud)+'", "longitud":"'+str(self._longitud)+'"}'}

        response = requests.post(URL_API + self._url, data=json.dumps(data), 
                                headers = headers)
        return response

    def set_ubicacion(self, latitud, longitud):
        self._latitud = latitud
        self._longitud = longitud

    def set_gasolina(self, gasolina):
        if gasolina < 20:
            self._llenar_tanque()
        else:
            self._gasolina = gasolina

    def get_gasolina(self):
        return self._gasolina

    def _llenar_tanque(self):
        self._gasolina= 100



vehiculos = []

"""Construye los vehiculos"""
for indice, variable_id in enumerate(VARIABLES_ID):
    vehiculo = Vehiculo(variable_id=variable_id, ruta=indice+1)
    vehiculos.append(vehiculo)


if __name__ == "__main__":
    """Ciclo principal"""
    while True:
        for vehiculo in vehiculos:
            vehiculo.conducir()
            vehiculo.reportar()
        time.sleep(2)
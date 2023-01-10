from main.map import ApuestaSchema
from main.repositories.repositorioapuesta import ApuestaRepositorio
from main.repositories.repositoriocuota import CuotaRepositorio
from abc import ABC
from Codigos.Prediccion import Prediccion
from scipy.stats import poisson
import pandas as pd

apuesta_schema = ApuestaSchema()
apuesta_repositorio = ApuestaRepositorio()
cuota_repositorio = CuotaRepositorio()

class ApuestaService:

    def __init__(self):
        self.df1 = pd.read_csv ('golesLigaVisitante.csv')
        self.df2 = pd.read_csv ('golesLigaLocal.csv')

    def agregar_apuesta(self, apuesta, local, visitante):
        cuota = cuota_repositorio.find_by_partido(apuesta)
        probabilidad = self.set_cuota(cuota, local, visitante)
        apuesta.ganancia = round(apuesta.monto * probabilidad, 2)
        return apuesta_repositorio.create(apuesta)

    def set_cuota(self, cuota, local, visitante):
        if local:
            cuota_local = CuotaLocal()
            probabilidad = cuota_local.calcular_cuota(cuota)
            return probabilidad
        if visitante:
            cuota_visitante = CuotaVisitante()
            probabilidad = cuota_visitante.calcular_cuota(cuota)
            return probabilidad
        cuota_empate = CuotaEmpate()
        probabilidad = cuota_empate.calcular_cuota(cuota)
        return probabilidad

    def obtener_apuesta_por_id(self, id):
        return apuesta_repositorio.find_one(id)

    def obtener_apuestas_ganadas(self):
        return apuesta_repositorio.find_wins()

    def obtener_apuestas(self):
        return apuesta_repositorio.find_all()

class CuotaStrategy(ABC):
    def calcular_cuota(self, local, visitante):
        """Calcular probabilidad"""
        if local in self.df2.index and visitante in self.df1.index:
            cuota_local = self.df2.at[local, 'Goles'] * self.df1.at[visitante, 'Goles']
            cuota_visitante = self.df1.at[visitante, 'Goles'] * self.df2.at[local, 'Goles']
            prob_local, prob_visitante, prob_empate= 0, 0, 0
            for x in range(0, 11): # Numero de goles del equipo local
                for y in range(0, 11): #Numero de goles del equipo visitante
                    p=poisson.pmf(x, cuota_local) * poisson.pmf(y, cuota_visitante)
                    if x==y:
                        prob_empate += p
                    elif x>y:
                        prob_local += p
                    else:
                        prob_visitante += p

            puntos_local = 3*prob_local + prob_empate
            puntos_visitante = 3*prob_visitante + prob_empate
            prob_local = round(puntos_local/(puntos_local + puntos_visitante), 2)
            prob_visitante = round(puntos_visitante/(puntos_local + puntos_visitante), 2)
            prob_empate = round(1 - prob_local - prob_visitante, 2)
            return (puntos_local, puntos_visitante)

        else:
            return (0, 0)


class CuotaLocal(CuotaStrategy):
    def calcular_cuota(self, cuota):
        probabilidad = cuota.cuota_local
        return probabilidad

class CuotaVisitante(CuotaStrategy):
    def calcular_cuota(self, cuota):
        probabilidad = cuota.cuota_visitante
        return probabilidad

class CuotaEmpate(CuotaStrategy):
    def calcular_cuota(self, cuota):
        probabilidad = cuota.cuota_empate
        return probabilidad
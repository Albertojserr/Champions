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


def obtenerEquipos(indice1,indice2):
    listaEquipos = pd.read_csv ('docs/equipo.csv')
    equipo1=listaEquipos['Equipo'][int(indice1-1)]
    equipo2=listaEquipos['Equipo'][int(indice2-1)]
    return equipo1,equipo2


class ApuestaService:

    def __init__(self):
        self.df1 = pd.read_csv('golesChampions.csv')
        self.df1= self.df1.set_index('Equipo')
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
    def calcular_cuota(self,local, visitante):
        """Calcular probabilidad"""
        if local in self.df1.index and visitante in self.df1.index:
            cuota_local = float(self.df1['golesLocal'][local]+1) * float(self.df1['golesRecibidosVisitante'][visitante]+1)
            cuota_visitante = float(self.df1['golesVisitante'][visitante]+1) * float(self.df1['golesRecibidosLocal'][local]+1)
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

            total=prob_empate+prob_local+prob_visitante
            prob_local=(prob_local*100)/total
            prob_empate=(prob_empate*100)/total
            prob_visitante=(prob_visitante*100)/total

            return (round(prob_local,2),round(prob_empate,2), round(prob_visitante,2))

        else:
            return (33,34,33)
    def cambiar_cuotas(self):
        listaPartidos = pd.read_csv ('docs/partidos.csv')

        for i in range(len(listaPartidos)):
            indice1=listaPartidos.iloc[i]['Local']
            indice2=listaPartidos.iloc[i]['Visitante']
            equipo1,equipo2=obtenerEquipos(indice1,indice2)
            prob=self.calcular_cuota(equipo1,equipo2)
            listaPartidos.iloc[i,3]=prob[0]
            listaPartidos.iloc[i,4]=prob[1]
            listaPartidos.iloc[i,5]=prob[2]
        listaPartidos.to_csv('docs/partidos.csv', index=False)


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
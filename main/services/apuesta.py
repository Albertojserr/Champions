from main.map import ApuestaSchema
from main.repositories.repositorioapuesta import ApuestaRepositorio
from main.repositories.repositoriocuota import CuotaRepositorio
from abc import ABC
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
        if local in self.df1.index and visitante in self.df1.index: #Si los equipos están en la base de datos
            cuota_local = float(self.df1['golesLocal'][local]+1) * float(self.df1['golesRecibidosVisitante'][visitante]+1) #Se calcula la cuota del equipo local
            cuota_visitante = float(self.df1['golesVisitante'][visitante]+1) * float(self.df1['golesRecibidosLocal'][local]+1) #Se calcula la cuota del equipo visitante
            prob_local, prob_visitante, prob_empate= 0, 0, 0 #Se inicializan las probabilidades de que gane el equipo local, el equipo visitante y que haya empate
            for x in range(0, 11): # Numero de goles del equipo local
                for y in range(0, 11): #Numero de goles del equipo visitante

                    #La distribución Poisson es una distribución de probabilidad discreta que expresa la probabilidad de que un evento
                    #ocurra un número determinado de veces en un intervalo de tiempo o espacio si ese evento ocurre con una tasa constante
                    #e independientemente del tiempo transcurrido desde el último evento.
                    #En este caso, el gol es el evento que puede ocurrir en los 90 minutos de un partido de fútbol.
                    #Hay 4 condiciones:
                    #      -El número de eventos se puede contar
                    #      -La ocurrencia de eventos son independientes
                    #      -La tasa a la que ocurren los eventos es constante
                    #      -Dos eventos no pueden ocurrir exactamente en el mismo instante de tiempo.
                    p=poisson.pmf(x, cuota_local) * poisson.pmf(y, cuota_visitante) #Se calcula la probabilidad de que el equipo local haga x goles y el equipo visitante haga y goles
                    if x==y: #Si el equipo local hace x goles y el equipo visitante hace y goles, se suma la probabilidad a la probabilidad de empate
                        prob_empate += p
                    elif x>y: #Si el equipo local hace x goles (más que el visitante) y el equipo visitante hace y goles, se suma la probabilidad a la probabilidad de que gane el equipo local
                        prob_local += p
                    else: #Si el equipo local hace x goles y el equipo visitante hace y goles (más que el local), se suma la probabilidad a la probabilidad de que gane el equipo visitante
                        prob_visitante += p

            total=prob_empate+prob_local+prob_visitante #Suma de todas las probabilidades, debe ser 1 (en porcentaje sería 100)
            prob_local=(prob_local*100)/total #Se convierte a porcentaje
            prob_empate=(prob_empate*100)/total #Se convierte a porcentaje
            prob_visitante=(prob_visitante*100)/total #Se convierte a porcentaje

            return (round(prob_local,2),round(prob_empate,2), round(prob_visitante,2)) #Se redondea a 2 decimales

        else:
            return (33,34,33) #Si no se encuentra el equipo en la base de datos, se devuelve una cuota de 33% para cada resultado
    def cambiar_cuotas(self):
        listaPartidos = pd.read_csv ('docs/partidos.csv') #Se lee el archivo csv con los partidos

        for i in range(len(listaPartidos)):
            indice1=listaPartidos.iloc[i]['Local'] #Se obtiene el indice del equipo local
            indice2=listaPartidos.iloc[i]['Visitante'] #Se obtiene el indice del equipo visitante
            equipo1,equipo2=obtenerEquipos(indice1,indice2) #Se obtienen los nombres de los equipos
            prob=self.calcular_cuota(equipo1,equipo2) #Se calcula la probabilidad de cada resultado
            listaPartidos.iloc[i,3]=prob[0] #Se actualizan las cuotas en el archivo csv
            listaPartidos.iloc[i,4]=prob[1]
            listaPartidos.iloc[i,5]=prob[2]
        listaPartidos.to_csv('docs/partidos.csv', index=False) #Se guarda el archivo csv con las nuevas cuotas


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
import pandas as pd


class Preparacion:

    def __init__(self):
        self.años=["2020-21","2019-20","2018-19","2017-18","2015-16","2014-15","2013-14","2012-13","2011-12","2010-11"]

        #primero sacamos todos los datos, los partidos entre equipos que sean de la seleccion, cojo los datos de goles, la lista de equipos, recorro los partidos de cada equipo y creo
        #dos arrays, la entrada son los goles de cada [1L,2V] y la salida el resultado del partido [n,m], luego se lo paso a la red neuronal para que pruebe
        self.listaEquipos = pd.read_csv ('docs/equipo.csv')
        self.equipos=self.listaEquipos['Equipo']
        self.partidos=pd.DataFrame(columns=['Local','GolesLocal','GolesVisitante','Visitante'])
        #self.partidos=self.partidos.append({'Local':'Real Madrid','GolesLocal':1,'GolesVisitante':2,'Visitante':'Barcelona'},ignore_index=True)

    def sacarDatos(self):
        for año in self.años:
            self.datos=pd.read_csv(f'Datos/Champions/resultados{año}.csv')
            self.merge = pd.merge(self.datos, self.listaEquipos , how='outer', indicator='resultado',sort=True, left_on='Local', right_on='Equipo')
            self.merge=self.merge[self.merge.resultado=='both'].drop('resultado',axis=1)
            self.partidos=self.partidos.append(self.merge,ignore_index=True)
            self.partidos=self.partidos.drop(['Equipo', 'Imagen', 'Pais', 'Indice'], axis=1)
            print(self.partidos)
        self.partidos.to_csv('docs/partidos.csv',index=False)

    def ejecutar():
        p=Preparacion()
        p.sacarDatos()

if __name__ == '__main__':

    Preparacion.ejecutar()






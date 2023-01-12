import pandas as pd


class Preparacion:

    def __init__(self):
        self.años=["2020-21","2019-20","2018-19","2017-18","2015-16","2014-15","2013-14","2012-13","2011-12","2010-11"]

        #primero sacamos todos los datos, los partidos entre equipos que sean de la seleccion, cojo los datos de goles, la lista de equipos, recorro los partidos de cada equipo y creo
        #dos arrays, la entrada son los goles de cada [1L,2V] y la salida el resultado del partido [n,m], luego se lo paso a la red neuronal para que pruebe
        self.listaEquipos = pd.read_csv ('docs/equipo.csv')
        self.equipos=list(self.listaEquipos['Equipo'])
        self.partidos=pd.DataFrame(columns=['Local','GolesLocal','GolesVisitante','Visitante'])

    def sacarDatos(self):
        for año in self.años:
            self.datos=pd.read_csv(f'Datos/Champions/resultados{año}.csv')
            for i in range(len(self.datos)):
                print(self.datos.iloc[i]['Local'])
                if str(self.datos.iloc[i]['Local']) in self.equipos:
                    if self.datos.iloc[i]['Visitante'] in self.equipos:
                        print(self.datos.iloc[i])
                        self.partidos=self.partidos.append({'Local':str(self.datos.iloc[i]['Local']),'GolesLocal':int(self.datos.iloc[i]['GolesLocal']),'GolesVisitante':int(self.datos.iloc[i]['GolesVisitante']),'Visitante':str(self.datos.iloc[i]['Visitante'])},ignore_index=True)

        print(self.partidos)

        self.partidos.to_csv('docs/partidosNeurona.csv',index=False)

    def ejecutar():
        p=Preparacion()
        p.sacarDatos()

if __name__ == '__main__':

    Preparacion.ejecutar()



import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt

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
                    if self.datos.iloc[i]['Visitante'] in self.equipos:#Guardamos los partidos en los que se enfrenten dos equipos de la lista de equipo.csv
                        self.partidos=self.partidos.append({'Local':str(self.datos.iloc[i]['Local']),'GolesLocal':int(self.datos.iloc[i]['GolesLocal']),'GolesVisitante':int(self.datos.iloc[i]['GolesVisitante']),'Visitante':str(self.datos.iloc[i]['Visitante'])},ignore_index=True)

        print(self.partidos)

        self.partidos.to_csv('docs/partidosNeurona.csv',index=False)

    def resultados(self):

        self.resultado=[]
        self.entrada=[]
        df1=pd.read_csv ('golesChampions.csv')
        df2=pd.read_csv ('golesLiga.csv')
        df1= df1.set_index('Equipo')
        df2= df2.set_index('Equipo')
        for i in range(len(self.partidos)):
            local=self.partidos.iloc[i]['Local']#sacamos el nombre del local, lo hacemos para que más tarde el código sea más limpio.
            visitante=self.partidos.iloc[i]['Visitante']
            datosLocal=[df1['golesLocal'][local],df1['golesRecibidosLocal'][local],df1['golesVisitante'][local],df1['golesRecibidosVisitante'][local],df2['golesLocal'][local],df2['golesRecibidosLocal'][local],df2['golesVisitante'][local],df2['golesRecibidosVisitante'][local]]
            datosVisitante=[df1['golesLocal'][visitante],df1['golesRecibidosLocal'][visitante],df1['golesVisitante'][visitante],df1['golesRecibidosVisitante'][visitante],df2['golesLocal'][visitante],df2['golesRecibidosLocal'][visitante],df2['golesVisitante'][visitante],df2['golesRecibidosVisitante'][visitante]]
            self.entrada.append([datosLocal[0],datosLocal[1],datosLocal[2],datosLocal[3],datosLocal[4],datosLocal[5],datosLocal[6],datosLocal[7],datosVisitante[0],datosVisitante[1],datosVisitante[2],datosVisitante[3],datosVisitante[4],datosVisitante[5],datosVisitante[6],datosVisitante[7]])
            self.resultado.append([self.partidos.iloc[i]['GolesLocal'],self.partidos.iloc[i]['GolesVisitante']])

    def redNeuronal(self):
        tf.keras.layers.Activation('relu')#Creamos la red neuronal que tendrá como función de activación la función relu. La hemos elegido porque es una función que para valor negativos sale 0 y para positivos el valor que tiene y en fútbol no hay valores negativos en el marcador.
        oculta1=tf.keras.layers.Dense(units=20,input_shape=[16])#la entrada de la red está en input_shape y son 16 parámetros
        oculta2=tf.keras.layers.Dense(units=20)#las capas ocultas
        oculta3=tf.keras.layers.Dense(units=20)
        oculta4=tf.keras.layers.Dense(units=20)
        oculta5=tf.keras.layers.Dense(units=20)
        salida=tf.keras.layers.Dense(units=2)#la capa de salida que son dos neuronas, goles de Local y goles de Visitante
        self.modelo=tf.keras.Sequential([oculta1,oculta2,oculta3,oculta4,oculta5,salida])
        self.modelo.compile(
            optimizer=tf.keras.optimizers.Adam(0.1),#Le ponemos 0.1 para que las correcciones de los pesos sean menores por lo que más precisas.
            loss='mean_squared_error' #Como función de pérdidas usamos la del error medio cuadrático.
        )

    def entrenar(self):
        print("Comenzando entrenamiento...")
        self.historial=self.modelo.fit(self.entrada,self.resultado,epochs=500,verbose=False)
        print("Modelo entrenado!")

    def graficar(self):
        plt.xlabel("# Epoca")
        plt.ylabel("Magnitud de perdida")#Vemos las pérdidas que va teniendo a lo largo de las distintas iteraciones que haga a los datos (epochs)
        plt.plot(self.historial.history["loss"])
        plt.show()

    def predecir(self):
        print("Hagamos una predicción!")
        print('Partido entre Atalanta y Villarreal')
        prueba=[1.8333333333333333,0.6666666666666666,1.1666666666666667,1.5,1.631578947368421,1.5263157894736843,1.7894736842105263,1.0,1.0,1.2222222222222223,0.5555555555555556,1.2222222222222223,2.1052631578947367,0.9473684210526315,1.2105263157894737,1.0]
        solucion=self.modelo.predict([prueba])
        print("El resultado es {}".format(solucion))
        a=round(solucion[0][0],0)
        b=round(solucion[0][1],0)
        print(f'El resultado es {a}-{b}')
        #Aquí después hay otros ejemplos comentados para probar la red neuronal, aunque si se prefiere se puede usar el .ipynb para mayor comodidad.
        '''
        print("Hagamos una predicción!")
        print('Partido entre Villarreal y Atalanta')
        prueba=[1.0,1.2222222222222223,0.5555555555555556,1.2222222222222223,2.1052631578947367,0.9473684210526315,1.2105263157894737,1.0,1.8333333333333333,0.6666666666666666,1.1666666666666667,1.5,1.631578947368421,1.5263157894736843,1.7894736842105263,1.0]
        solucion=modelo.predict([prueba])
        print("El resultado es {}".format(solucion))
        a=round(solucion[0][0],0)
        b=round(solucion[0][1],0)
        print(f'El resultado es {a}-{b}')
        '''

        '''
        print("Hagamos una predicción!")
        print('Partido entre Barcelona y Bayern')
        prueba=[2.4126984126984126,0.6825396825396826,1.5714285714285714,1.0317460317460319,1.9473684210526316,1.0,1.631578947368421,1.0,2.3684210526315788,0.631578947368421,1.3333333333333333,1.5614035087719298,2.823529411764706,0.8823529411764706,2.8823529411764706,1.2941176470588236]
        solucion=modelo.predict([prueba])
        print("El resultado es {}".format(solucion))
        a=round(solucion[0][0],0)
        b=round(solucion[0][1],0)
        print(f'El resultado es {a}-{b}')
        '''
    def ejecutar():
        p=Preparacion()
        p.sacarDatos()
        p.resultados()
        p.redNeuronal()
        p.entrenar()
        p.graficar()
        p.predecir()

if __name__ == '__main__':

    Preparacion.ejecutar()



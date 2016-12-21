# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 19:54:31 2016

@author: ponco
"""


import pandas as pd
import matplotlib.pyplot as plt
#import json, codecs

"""

LIMPIEZA

"""


estaciones = pd.read_json('ecobici/stations.json', orient="records")
id_max_estacion = estaciones["id"].max()
datos = pd.read_pickle('ecobici/databici.pkl')
##datos_sep = pd.read_pickle('ecobici/2016-09.pkl')
#datos_sep = pd.read_csv(filepath_or_buffer = 'ecobici/2016-09.csv', encoding = 'utf-8', sep = ';', parse_dates={"Retiro":[4,5], "Arribo":[7,8]}, dayfirst=True)
##datos_oct = pd.read_csv(filepath_or_buffer = 'ecobici/2016-10.csv', encoding = 'utf-8', sep = ',', parse_dates=[4,7], infer_datetime_format=True, dayfirst=True) #dataset corrupto
##hora = 0
##lminutos = 0
##hreset = False
##for idx,dato in datos_oct["Hora_Retiro"].iteritems():
##    if dato.count(":") == 2:
##        sdato = dato.split(':')
##        hora = int(sdato[0])
##        lminutos = int(sdato[1])
##        continue
##    if hora == 0:
##        hreset = True
##    try:
##        minutos = int(dato[:2])
##    except:
##        dato = dato.split(':', 1)[1]
##        minutos = int(dato[:2])
##        
##    if lminutos > minutos:
##        if hreset:
##            hora = 4
##            hreset = False
##        hora = (hora + 1) % 24
##    lminutos = minutos
##    dato = '{:02d}:'.format(hora) + dato
##    datos_oct.set_value(idx, "Hora_Retiro", dato)
##datos_oct = pd.read_csv(filepath_or_buffer = 'ecobici/2016-10_repair.csv', encoding = 'utf-8', sep = ',', parse_dates={"Retiro":[4,5], "Arribo":[7,8]}, dayfirst=True)
#datos_oct = pd.read_pickle('ecobici/2016-10.pkl')
#datos_nov = pd.read_csv(filepath_or_buffer = 'ecobici/2016-11.csv', encoding = 'utf-8', sep = ',', parse_dates={"Retiro":[4,5], "Arribo":[7,8]}, infer_datetime_format=True)
#
#
#
#
#"""
#
#GENERAR DATOS DE TIEMPO
#
#
#"""
#
#
#datos = pd.concat([datos_sep, datos_oct, datos_nov], ignore_index=True)
#datos["HoraMil_Arr"] = datos["Arribo"].apply(lambda x: pd.to_datetime(x).hour*100 + pd.to_datetime(x).minute)
#datos["HoraMil_Ret"] = datos["Retiro"].apply(lambda x: pd.to_datetime(x).hour*100 + pd.to_datetime(x).minute)
#datos["DiaDelAño_Arr"] = datos["Arribo"].apply(lambda x: pd.to_datetime(x).dayofyear)
#datos["DiaDelAño_Ret"] = datos["Retiro"].apply(lambda x: pd.to_datetime(x).dayofyear)
#
#datos_arribo = pd.merge(left = datos, right = estaciones, how='inner', left_on='Ciclo_Estacion_Arribo', right_on='id')
#
#
#"""
#
##HACER BINNEADO
#
#"""
#
#
#def binnear(d):
#    if 500<= d <1000:
#        return "Mañana"
#    if 1000<= d <1500:
#        return "MedioDía"
#    if 1500<= d <2000:
#        return "Tarde"
#    return "Noche"
##datos["Bin_Arr"] = pd.cut(datos["HoraMil_Arr"], bins, labels=etiquetas)
##datos["Bin_Ret"] = pd.cut(datos["HoraMil_Ret"], bins, labels=etiquetas)
#datos["Bin_Arr"] = datos["HoraMil_Arr"].apply(binnear)
#datos["Bin_Ret"] = datos["HoraMil_Ret"].apply(binnear)

datos_arribo = pd.merge(left = datos, right = estaciones, how='inner', left_on='Ciclo_Estacion_Arribo', right_on='id')


"""

GRAFICAR AFLUENCIA

"""

afluencia_total = datos_arribo["name"].value_counts()
afluencia_total[0:20].plot(kind='bar')


"""

GENERAR DATASET PARA CLUSTERING

"""

arribos = datos[["Ciclo_Estacion_Arribo", "HoraMil_Arr", "Bin_Arr"]].groupby("Ciclo_Estacion_Arribo")
retiros = datos[["Ciclo_Estacion_Retiro", "HoraMil_Ret", "Bin_Ret"]].groupby("Ciclo_Estacion_Retiro")

arribos_etiq = arribos["Bin_Arr"].value_counts()
retiros_etiq = retiros["Bin_Ret"].value_counts()

arribos_binneados = pd.DataFrame()
retiros_binneados = pd.DataFrame()

map( lambda x: arribos_binneados.set_value(x[0][0],x[0][1], x[1]) , arribos_etiq.iteritems() )
map( lambda x: retiros_binneados.set_value(x[0][0],x[0][1], x[1]) , retiros_etiq.iteritems() )

arribos_binneados = arribos_binneados.reindex(columns=["Mañana","MedioDía","Tarde","Noche"]).fillna(0)
retiros_binneados = retiros_binneados.reindex(columns=["Mañana","MedioDía","Tarde","Noche"]).fillna(0)

arribos_binneados.T.plot(title = "Arribos", legend = False)
retiros_binneados.T.plot(title = "Retiros", legend = False)

input_clasificador = pd.merge(left = arribos_binneados, right = retiros_binneados, left_index = True, right_index = True, suffixes=('_Arr', '_Ret'))
input_clasificador.to_csv('ecobici/clustering.csv')


"""

GRAFICAR MATRIZ DE CORRELACION

"""
plt.figure()
clas_corr = input_clasificador.corr()
plt.pcolor(clas_corr, cmap=plt.cm.Reds)
#plt.yticks(range(len(clas_corr.index)), clas_corr.index)
#plt.xticks(range(len(clas_corr.columns)), clas_corr.columns)



"""

GRAFICAR USO DIARIO

"""

arribos_tiempo = datos[["Ciclo_Estacion_Arribo","HoraMil_Arr", "DiaDelAño_Arr", "Bin_Arr"]].groupby("Ciclo_Estacion_Arribo")
arribos_plot=arribos_tiempo["DiaDelAño_Arr"].value_counts()
plt.figure()
tendencias = pd.Series()

for i in range(1, id_max_estacion + 1):
    temp = arribos_plot.loc[i].sort_index()
    temp.plot(title="Arribos por dia")
    xt = pd.Series(temp.index)
    yt = temp.reset_index(drop=True)
    regression = pd.ols(x=xt, y=yt)
    #print(regression.beta[0])
    tendencias = tendencias.set_value(i, regression.beta[0])
    #trend = regression.predict(beta=regression.beta, x=xt) 
    #data = pd.DataFrame(index=xt, data={'y': yt.values, 'trend': trend.values})
    #data.plot(title="Arribos por dia")
    #raw_input()

"""

GRAFICAR TENDENCIAS TEMPORALES

"""

tendencias = pd.merge(left=pd.DataFrame(tendencias.sort_values()), right=estaciones[["id","name"]], how='inner', left_index=True, right_on='id' ).rename(columns={0:"Tendencia"})
pd.Series(data=tendencias["Tendencia"].values, index=tendencias["name"]).plot(title="Tendencias")
pd.Series(data=tendencias["Tendencia"].values, index=tendencias["name"])[-20:].plot(title="Tendencias a la alta", kind='bar')
pd.Series(data=tendencias["Tendencia"].values, index=tendencias["name"])[:20].plot(title="Tendencias a la baja", kind='bar')
            
    
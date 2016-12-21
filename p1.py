# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 14:03:07 2016

@author: ponco
"""

import pandas as pd
import matplotlib.pyplot as plt

"""

Limpieza

"""

datos = pd.read_csv(filepath_or_buffer = 'nacimientos/conjunto_de_datos/resultados_ageb_urbana_09_cpv2010.csv', encoding = 'utf-8', na_values="*")
#datos = datos[datos.columns].apply(lambda x: pd.to_numeric(x, errors='ignore'))
columnas_edades = ["p_0a2", "p_3a5",  "p_6a11",  "p_8a14", "p_15a17",  "p_18a24", "p_15a49"]
columnas_edades_m = [x+"_m" for x in columnas_edades[:-1]]
columnas_edades_f = [x+"_f" for x in columnas_edades[:-1]]
datos_alvaro = datos[ (datos["nom_mun"] == u"Álvaro Obregón") & (datos["nom_loc"] == u"Total AGEB urbana")]
#datos_alvaro[columnas_edades + columnas_edades_f + columnas_edades_m] = datos_alvaro[columnas_edades + columnas_edades_f + columnas_edades_m].apply(lambda x: pd.to_numeric(x, errors='coerce'))
#datos_alvaro[columnas_edades].plot()

"""

Grafica de mujeres

"""

datos_alvaro[columnas_edades_f].plot()


"""

Grafica piramide poblacional

"""


fig, axes = plt.subplots(ncols=2, sharey="row")
y = range(len(columnas_edades)-1)

axes[0].barh(y, datos_alvaro[columnas_edades_f].values[0], align='center')
axes[0].set(title="Mujeres")
axes[1].barh(y, datos_alvaro[columnas_edades_m].values[0], align='center',color="red")
axes[1].set(title="Hombres")

axes[0].invert_xaxis()
axes[0].set(yticks=y, yticklabels=columnas_edades)
axes[0].yaxis.tick_right()
fig.tight_layout()
fig.subplots_adjust(wspace=0.11)
plt.show()

phombre = 0.5039
pmujer = 1 - phombre

mujeres = datos_alvaro[columnas_edades_f+["p_15a49_f"]].fillna(0)
mujeres["p_24a49_f"] = mujeres["p_15a49_f"] - (mujeres["p_15a17_f"]+mujeres["p_18a24_f"])
mujeres.drop('p_15a49_f', axis=1, inplace=True)

tasa_abs = pd.Series(data=[156064, 160715, 160022, 155070, 161032, 158272, 155007, 145847, 146383, 137249 ], index=range(2006,2016))/194612
perdida_por_2y = pd.Series(data=[1.0, 1.0, 1/6.0, 1/6.0, 1.0, 1/6.0, 1/13.0], index=mujeres.columns) #considerando overlapping 
coef_natalidad = pd.Series(data=[0.0, 0.0, 0.0, 0.0, 0.04, 0.11, 0.25], index=mujeres.columns)

tasa_abs_prom = [0.8203, 0.7729, 0.7287]


for idx, ageb in mujeres.T.iteritems():
    for i in range(3):
        nuevos = (tasa_abs_prom[i] * coef_natalidad * ageb).sum()*pmujer
        perdida =  (ageb * perdida_por_2y)
        ageb -= perdida
        perdida = perdida.shift(1)
        perdida.iloc[0] = nuevos
        ageb += perdida

mujeres["niños_6meses_2016"]=mujeres["p_0a2_f"]/4
plt.figure()
mujeres["niños_6meses_2016"].plot()
        
    
    
    
    

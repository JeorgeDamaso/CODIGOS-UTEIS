import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
import os
import re
import pandas as pd
#############################################################################################
##################################################CAPITURA DE DADOS DE UMA RAIZ ESPECIFICA###
#############################################################################################
caminho = '/home/darkario/Transferências/CURSOS_COMPUTACAO'
lista2 = []
lista_caminho = []
lista_nome = []
lista = [i for x,y,i in os.walk(caminho)]
for diretorio,pasta,aquivos in os.walk(caminho):

    for arquivo in aquivos:
            #nome do arquivo
            lista2.append(arquivo)
                #nome do caminho                    
            lista_caminho.append(str(os.path.join(os.path.realpath(diretorio), arquivo)))
                    #nome absoluto do arquivo
            lista_nome.append(os.path.basename(str(os.path.join(os.path.realpath(diretorio), arquivo))))

base_dados = pd.DataFrame(pd.Series(lista_caminho))

####################################################################################
######################################ORGANIZANDO COLUNAS A PARTI DA RAIZ, SUBDIRETORIO
#####################################E NOMES DE ARQUIVOS
######################################################################################

base_dados["curso"]=base_dados[0].str.findall('pasta_raiz aqui/([\S ]+?)/').str.get(0)
base_dados['arquivo'] = lista_nome
base_dados['suporte'] = base_dados['arquivo'].str.findall('[0-9]+').str.get(0)
base_dados['extensao'] = base_dados['arquivo'].str.findall('.[0-9a-zA-Z]+$').str.get(0).str.lower()
base_dados['modulo'] = base_dados[0].str.split(os.sep).str.get(-2)
base_dados['tamanho em B'] = [os.stat(x)[6] for x in lista_caminho]


base_dados = base_dados[[0,'curso', 'suporte', 'modulo', 'arquivo', 'extensao', 'tamanho em B']]
base_dados.drop_duplicates()
####################################################################################
#########################GERANDO GRAFICOS##########################################

a = base_dados.loc[base_dados['extensao'].str.contains('.MP4|.mp4|.rmbv|avi', regex=True)]

a = a.groupby(['curso', 'extensao'])['tamanho em B'].sum().reset_index()
a['tamanho em B'] = a['tamanho em B']/10**9

fig = plt.figure(figsize=(15,20))
grade=(9,15)

############################################

ax = plt.subplot2grid(grade, (0,0),rowspan=4,colspan=6, fig=fig)
for x,_,y in list(a.values):
    ax.barh(x, y)
ax.set_xlabel('Tamanho em GB')
for x in range(len(a.curso)):
    plt.annotate(f"{a['tamanho em B'].values[x].round(2)} GB", xy=(a['tamanho em B'].values[x], x-0.2), size=15)
ax.set_title('tamanho dos cursos em GB', size=20)
plt.yticks(size=20)
#############################################################

ax1 = plt.subplot2grid(grade, (0,8), fig=fig, rowspan=15, colspan=6)
graf_ax1 = base_dados.groupby('extensao')['tamanho em B'].count().reset_index()

for x in graf_ax1.values:
    ax1.barh(x[0], x[1])
    plt.annotate(x[1], xy=(x[1]+0.8, list(graf_ax1['tamanho em B'].values).index(x[1])-0.3), size=20)
#for x in gra_ax1.vales:
#    plt.ann
plt.xscale('log')
plt.title('QUANTIDADE TOTAL\n POR TIPO DE ARQUIVO', size=20)
plt.yticks(size=20)
#    ax1.annotate(x[y], xy=(list(sub.values()).index[y], x[y]))
#cmap = cm.get_cmap('Spectral')
#base_dados.groupby('extensao')['extensao'].count().plot(kind='barh',cmap=cmap, log=True, ax=ax1)

##############################################################

ax2 = plt.subplot2grid(grade, (5,0), fig=fig, rowspan=15, colspan=6)
calculo = base_dados[['curso','modulo']].drop_duplicates().groupby('curso')['modulo'].count().sort_values(ascending=False)

calculo.plot(kind='barh', ax=ax2)
for x in calculo.reset_index().values:
    ax2.annotate(f'{x[1]} UN', xy=(x[1], list(calculo).index(x[1])),size=15)
plt.yticks(size=20)
plt.title('quantidade de modulos', size=20)

#################guardar dataset
pd.DataFrame(base_dados).to_csv("/home/darkario/Desktop/cursos.csv")

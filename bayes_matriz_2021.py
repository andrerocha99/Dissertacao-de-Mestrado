import pandas as pd
from pgmpy.models import BayesianModel

ataques = pd.read_excel(r'C:\Users\35192\Desktop\Tese\Criar Base de Dados\BD apos o pre-processamento\BD Finais\crua.xlsx')


ataques = ataques[['Risco_Bandeira','Nível_Proteção','Estado do Navio','Tipo_Navio',
                    'Nível_Ataque','Ano','Período','Estação_Africa','Meteorologia','Estado_Costeiro',
                    'Perigosidade','ÁREA_NAVEGAÇÃO']]


#Para prever qual o risco de ataque

model_nivel_ataque = BayesianModel([('Risco_Bandeira', 'Nível_Proteção'),
                        ('Estado do Navio','Nível_Proteção'),
                        ('Tipo_Navio','Nível_Proteção'),
                        ('Nível_Proteção','Nível_Ataque'),
                        ('Ano','Nível_Ataque'),
                        ('Período','Nível_Ataque'),
                        ('Estação_Africa','Meteorologia'),
                        ('Meteorologia','Nível_Ataque'),
                        ('Estado_Costeiro','Perigosidade'),
                        ('ÁREA_NAVEGAÇÃO','Nível_Ataque'),
                        ('Perigosidade','Nível_Ataque')])
model_nivel_ataque.fit(ataques)

labels_to_use = list(model_nivel_ataque.nodes)

dados_rede = ataques[labels_to_use]
predict_nivel = dados_rede.drop(columns='Nível_Ataque')


Previsão = model_nivel_ataque.predict(predict_nivel)
Probabilidade_Nivel = model_nivel_ataque.predict_probability(predict_nivel) #para mostrar as probabilidades de cada corresponder a cada um dos possíveis acontecimento



dados_rede['previsão_nivel']=Previsão

previsão_nivel = pd.crosstab(dados_rede['Nível_Ataque'],dados_rede['previsão_nivel']) #para ver a matriz de dupla-entrada e calcular a precisão do modelo

print(previsão_nivel)




#prever para 2021



ataques_t1 = pd.read_excel(r'C:\Users\35192\Desktop\Tese\Criar Base de Dados\BD apos o pre-processamento\Base_Dados_7_to.xlsx')

ataques_t1 = ataques_t1[['Risco_Bandeira','Nível_Proteção','Estado do Navio','Tipo_Navio',
                    'Nível_Ataque','Ano','Período','Estação_Africa','Meteorologia','Estado_Costeiro',
                    'Perigosidade','ÁREA_NAVEGAÇÃO']]

ataques_t2 = ataques_t1[564:]

ataques_t2 = ataques_t2[labels_to_use]

a_prever = ataques_t2[labels_to_use].drop(columns='Nível_Ataque')

Previsão_t = model_nivel_ataque.predict(a_prever)

ataques_t2['previsão_nivel'] = Previsão_t.values

previsão_nivel_t = pd.crosstab(ataques_t2['Nível_Ataque'],ataques_t2['previsão_nivel']) #para ver a matriz de dupla-entrada e calcular a precisão do modelo

print(previsão_nivel_t)
difference = abs(dados_rede['Nível_Ataque']-dados_rede['previsão_nivel'])

ataques_mal_previstos = dados_rede[difference != 0]

#ataques_mal_previstos.to_excel('bases dados corrigida por bayes.xlsx')




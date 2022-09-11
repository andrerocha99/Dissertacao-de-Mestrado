import pandas as pd
from pgmpy.models import BayesianModel

ataques = pd.read_excel(r'C:\Users\35192\Desktop\Tese\Criar Base de Dados\BD apos o pre-processamento\Base_Dados_5.xlsx')



ataques = ataques[['Risco_Bandeira','Nível_Proteção','Estado do Navio','Tipo_Navio',
                   'Nível_Ataque','Ano','Período','Estação_Africa','Meteorologia','Estado_Costeiro',
                   'Perigosidade','ÁREA_NAVEGAÇÃO','Sucesso_Ataque']]
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

difference = abs(dados_rede['Nível_Ataque']-dados_rede['previsão_nivel'])

ataques_mal_previstos = dados_rede[difference != 0]

#ataques_mal_previstos.to_excel('fogoooo.xlsx')
dados_rede.to_excel('corrigido bayes com 2021.xlsx')


#Para prever se o ataque tem sucesso ou não

model_sucesso_ataque = BayesianModel([('Risco_Bandeira', 'Nível_Proteção'),
                        ('Estado do Navio','Nível_Proteção'),
                        ('Tipo_Navio','Nível_Proteção'),
                        ('Nível_Proteção','Sucesso_Ataque'),
                        ('Ano','Sucesso_Ataque'),
                        ('Período','Sucesso_Ataque'),
                        ('Estação_Africa','Meteorologia'),
                        ('Meteorologia','Sucesso_Ataque'),
                        ('Estado_Costeiro','Perigosidade'),
                        ('ÁREA_NAVEGAÇÃO','Sucesso_Ataque'),
                        ('Perigosidade','Sucesso_Ataque')])
 
model_sucesso_ataque.fit(ataques)

variables_to_use = list(model_sucesso_ataque.nodes)

dados_rede_sucesso = ataques[variables_to_use]
predict_sucesso = dados_rede_sucesso.drop(columns='Sucesso_Ataque')


Previsão_2 = model_sucesso_ataque.predict(predict_sucesso)
Probabilidade_Sucesso = model_sucesso_ataque.predict_probability(predict_sucesso)

dados_rede_sucesso['Previsão_Sucesso']=Previsão_2
sucesso = pd.crosstab(dados_rede_sucesso['Sucesso_Ataque'],dados_rede_sucesso['Previsão_Sucesso'])
print(sucesso)

#for cpd in model1.get_cpds():   
    #print("CPD of {variable}:".format(variable=cpd.variable))
    #print(cpd)


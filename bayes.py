import pandas as pd
from pgmpy.models import BayesianModel

ataques = pd.read_excel(r'C:\Users\35192\Desktop\Tese\Criar Base de Dados\BD apos o pre-processamento\Base_Dados_4.xlsx')

#Para prever qual o risco de ataque

model_risco_ataque = BayesianModel([('Risco_Bandeira', 'Nível_Proteção'),
                        ('Estado do Navio','Nível_Proteção'),
                        ('Tipo_Navio','Nível_Proteção'),
                        ('Nível_Proteção','Risco_Ataque'),
                        ('Ano','Risco_Ataque'),
                        ('Período','Risco_Ataque'),
                        ('Estação','Meteorologia'),
                        ('Meteorologia','Risco_Ataque'),
                        ('Estado_Costeiro','Perigosidade'),
                        ('ÁREA_NAVEGAÇÃO','Risco_Ataque'),
                        ('Perigosidade','Risco_Ataque')])
model_risco_ataque.fit(ataques)

labels_to_use = list(model_risco_ataque.nodes)

dados_rede = ataques[labels_to_use]
predict_risco = dados_rede.drop(columns='Risco_Ataque')


Previsão = model_risco_ataque.predict(predict_risco)
Probabilidade_Risco = model_risco_ataque.predict_probability(predict_risco) #para mostrar as probabilidades de cada corresponder a cada um dos possíveis acontecimento



dados_rede['Previsão_Risco']=Previsão

previsão_risco = pd.crosstab(dados_rede['Risco_Ataque'],dados_rede['Previsão_Risco']) #para ver a matriz de dupla-entrada e calcular a precisão do modelo


#Para prever se o ataque tem sucesso ou não

model_sucesso_ataque = BayesianModel([('Risco_Bandeira', 'Nível_Proteção'),
                        ('Estado do Navio','Nível_Proteção'),
                        ('Tipo_Navio','Nível_Proteção'),
                        ('Nível_Proteção','Sucesso_Ataque'),
                        ('Ano','Sucesso_Ataque'),
                        ('Período','Sucesso_Ataque'),
                        ('Estação','Meteorologia'),
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


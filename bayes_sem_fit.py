import pandas as pd
import numpy as np
from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

ataques = pd.read_excel(r'C:\Users\35192\Desktop\Tese\Criar Base de Dados\BD apos o pre-processamento\Base_Dados_4.xlsx')

#definir as relações entre as variáveis
model = BayesianModel([('Risco_Bandeira', 'Nível_Proteção'),
                       ('Estado do Navio','Nível_Proteção'),
                       ('Tipo_Navio','Nível_Proteção'),
                       ('Nível_Proteção','Risco_Ataque'),
                       ('Meteorologia','Risco_Ataque'),
                       ('Perigosidade','Risco_Ataque')])

Estado_Navio = TabularCPD(variable='Estado do Navio', variable_card=3,
                          values=[[0.046],[0.463],[0.491]])

Risco_Bandeira = TabularCPD(variable='Risco_Bandeira', variable_card=3,
                             values=[[0.294],[0.564],[0.142]])

Tipo_Navio = TabularCPD(variable='Tipo_Navio', variable_card=4,
                        values=[[0.351],[0.411],[0.105],[0.133]])


#Nível_Proteção = TabularCPD(variable='Nível_Proteção', variable_card=3,
                            #values=[[0.647],[0.248],[0.105]])

Nível_Proteção = TabularCPD(variable='Nível_Proteção',variable_card=3,
                            values=[[0.8,0.886,0.527,1,1,0.7,1,0.911,0.417,0,0.765,0.5,0.33,0.6,1,0.33,0.9,0.286,0.667,0.69,0.383,0.5,0.571,0.333,1,0.697,0.479,0.5,0.866,0.63,0.33,0.33,0.5,0.33,0.929,0.385],
                                    [0.2,0.098,0.4,0,0,0.2,0,0.067,0.472,0,0.176,0.25,0.33,0.2,0,0.33,0.1,0.428,0,0.19,0.383,0.5,0.286,0.417,0,0.182,0.375,0.5,0.067,0.259,0.33,0.33,0.5,0.33,0,0.538],
                                    [0,0.016,0.073,0,0,0.1,0,0.022,0.111,1,0.059,0.25,0.34,0.2,0,0.34,0,0.286,0.333,0.120,0.234,0,0.143,0.25,0,0.121,0.146,0,0.067,0.111,0.34,0.34,0,0.34,0.071,0.077]],
                            evidence=['Tipo_Navio','Risco_Bandeira','Estado do Navio'],
                            evidence_card=[4,3,3])

Meteorologia = TabularCPD(variable='Meteorologia', variable_card=3,
                          values=[[0.124],[0.81],[0.066]])

Perigosidade = TabularCPD(variable='Perigosidade', variable_card=3,
                          values=[[0.087],[0.461],[0.452]])

#Risco_Ataque = TabularCPD(variable='Risco_Ataque', variable_card=3,
                                  #values=[[0.133],[0.420],[0.447]])

Risco_Ataque = TabularCPD(variable='Risco_Ataque', variable_card=3,
                                  values=[[0.333,0.111,0.333,0.667,0.385,0.5,1,0.2,0.625,1,0.229,0,0.8,0.375,0.68,0.828,0.208,0.746,0.333,0,0.333,0.333,0.5,0.5,0.5,0.278,0.5],
                                          [0.333,0.889,0.333,0.333,0.577,0.333,0,0.667,0.25,0,0.771,1,0.2,0.493,0.3,0.143,0.455,0.224,0.333,1,0.333,0.333,0.333,0,0.5,0.222,0.333],
                                          [0.334,0,0.334,0,0.038,0.167,0,0.133,0.125,0,0,0,0,0.132,0.02,0.029,0.337,0.03,0.334,0,0.334,0.334,0.167,0.5,0,0.5,0.167]],
                                  evidence=['Nível_Proteção','Meteorologia','Perigosidade'],
                                  evidence_card=[3,3,3])



model.add_cpds(Risco_Bandeira, Estado_Navio, Tipo_Navio, Nível_Proteção, Meteorologia, Perigosidade, Risco_Ataque)

for cpd in model.get_cpds():   #para mostrar as probabilidades de cada acontecimento
    print("CPD of {variable}:".format(variable=cpd.variable))
    print(cpd)

model.check_model() #para verificar se o modelo construído tem erros

risco_ataque_inference = VariableElimination(model)

for i in range(3):
    print('evidence= '+ str(i))
    print(risco_ataque_inference.query(variables=['Risco_Ataque'],evidence={'Nível_Proteção':i})
)

prob_risco_ataque = risco_ataque_inference.query(variables=['Risco_Ataque'])
print(prob_risco_ataque['Risco_Ataque'])


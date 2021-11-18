import pandas as pd
df = pd.read_csv(r'C:\Users\35192\Desktop\Tese\Criar Base de Dados\BD apos o pre-processamento\Base_Dados_1.csv')

df.info() #para ver quantos missing value por cada variável

#Separar os missing values da variável Bandeira e N_Criminosos para serem o conjunto de teste
test_data1 = df[df["Bandeira"].isnull()]
test_data2 = df[df["N_Criminosos"].isnull()]

#Eliminar os missing values da df (foram eliminados o num criminoso e o EB, considerar como train data
df.dropna(inplace=True)

#train data = rows from df where columns "Bandeira" e "N_Criminosos" não têm missing values

#df.isnull.sum() #confirma que não tenho missing values no train dataset

y_train1 = df["Bandeira"] #representa as rows da df com a variável Bandeira que não tem missing values
y_train2 = df["N_Criminosos"] #representa as rows da df com a variável N_Criminosos que não tem missing values

#x_train é a base de dados sem Bandeira e N_Criminosos sem conter quaisquer valores omissos
x_train1 = df.drop("Bandeira",axis=1) 
x_train2 = df.drop("N_Criminosos",axis=1)

from sklearn.linear_model import LinearRegression
lr = LinearRegression()

#treinar o modelo

lr.fit(x_train1, y_train1)
lr.fit(x_train2, y_train2)


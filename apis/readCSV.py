import pandas as pd

# parsing 하여 만든 csv파일 dataframe 변수화

df_regionCode      = pd.read_csv('../csv/regionCode_encode.csv', encoding='utf-8')
df_animalHospital  = pd.read_csv('../csv/animalHospital.csv', encoding='utf-8')
df_familyIncome    = pd.read_csv('../csv/familyIncome.csv', encoding='utf-8')
df_medicalExpense  = pd.read_csv('../csv/medicalExpense_neutering.csv', encoding='utf-8')
df_abandonedAnimal = pd.read_csv('../csv/abandonedAnimal.csv', encoding='utf-8')
df_petData         = pd.read_csv('../csv/petData.csv', encoding='utf-8')

#print(df_regionCode)
#print(df_animalHospital)
#print(df_familyIncome)
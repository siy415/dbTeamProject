import pandas as pd

df_regionCode = pd.read_csv('../../regionCode_encode.csv', encoding='utf-8')
df_animalHospital = pd.read_csv('../../animalHospital.csv', encoding='utf-8')
df_familyIncome = pd.read_csv('../../familyIncome.csv', encoding='utf-8')

print(df_regionCode)
print(df_animalHospital)
print(df_familyIncome)
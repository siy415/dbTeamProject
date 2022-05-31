from configparser import LegacyInterpolation
import math
from operator import le
from tkinter.messagebox import NO
import pymysql
import readCSV
import pandas as pd
from sqlalchemy import create_engine

conn = pymysql.connect(host='localhost', user='root', passwd='autoset',charset='utf8',database='teamProject')

l_code = {

}

pymysql.install_as_MySQLdb()

cursor = conn.cursor()

engine = create_engine(f"mysql+mysqldb://{'root'}:{'autoset'}"\
                    f"@{'localhost'}:3306/{'teamProject'}",
                    encoding="utf-8")

# cursor.execute("show databases")

# a = cur.fetchall()

def insertRegionInfo(): 
    df_regionCode = readCSV.df_regionCode
    df_familyIncome = readCSV.df_familyIncome
    df_medicalExpense = readCSV.df_medicalExpense

    # print(df_regionCode)

    df_familyIncome = df_familyIncome.rename(columns={"legal_code": "legal_code_"})
    df = pd.merge(df_regionCode, df_familyIncome, left_on="legal_code", right_on="legal_code_", how="left").drop(columns='legal_code_')
    #print(df)
    df = pd.merge(df, df_medicalExpense, on="name", how="left")
    df = df.astype(object).where(pd.notnull(df), 0)

    #print(df)

    df.to_sql(con=engine, if_exists="append", index=False, name='region_info')

    #for idx, row in df.iterrows():
    #    print(type(row.legal_code), type(row.neutering_price), type(row.income_level))
    #    cursor.execute("INSERT INTO `region_info` (legal_code,name,income_level,exist,neutering_price) values(?,?,?,?,?)", (row.legal_code, row.name, row.income_level, row.exist, row.neutering_price))

    # conn.commit()

    print("%s done" % insertRegionInfo.__name__)

def insertAbandonedAnimal():
    df_abandonedAnimal = readCSV.df_abandonedAnimal

    print(df_abandonedAnimal)
    for idx, row in df_abandonedAnimal.iterrows():
        s = row.kind.split(" ")[0].strip('[').strip(']')
        row.kind = s
        df_abandonedAnimal.loc[idx, 'kind'] = s

        if row.legal_code in l_code:
                df_abandonedAnimal.loc[idx, 'legal_code'] = l_code[row.legal_code]
        else:
            cursor.execute("select legal_code from region_info where name=%s", (row.legal_code))
            s = cursor.fetchone()[0]
            df_abandonedAnimal.loc[idx, 'legal_code'] = s

        # print(df_abandonedAnimal.loc[idx])

    #print(df_abandonedAnimal)

    df_abandonedAnimal = df_abandonedAnimal.astype(object).where(pd.notnull(df_abandonedAnimal), 0)

    df_abandonedAnimal.to_sql(con=engine, if_exists="append", index=False, name='abandoned_animal')

    print("%s done" % insertAbandonedAnimal.__name__)

def insertHospital():
    df_animalHospital = readCSV.df_animalHospital

    print(df_animalHospital)
    for idx, row in df_animalHospital.iterrows():
        if row.legal_code == row.legal_code:
            split = row.legal_code.split(' ')
            legal_code = split[0] + ' ' + split[1]
            if legal_code in l_code:
                df_animalHospital.loc[idx, 'legal_code'] = l_code[legal_code]
            else:
                # print(legal_code)
                cursor.execute("select legal_code from region_info where name=%s", (legal_code))
                s = cursor.fetchone()[0]
                df_animalHospital.loc[idx, 'legal_code'] = s
        else:
            df_animalHospital.loc[idx, 'legal_code'] = 0

        # print(df_animalHospital.loc[idx])

    #print(df_animalHospital)
    df_animalHospital = df_animalHospital.astype(object).where(pd.notnull(df_animalHospital), 0)

    df_animalHospital.to_sql(con=engine, if_exists="append", index=False, name='animal_hospital')

    print("%s done" % insertHospital.__name__)

def insertPetData():
    df_petData = readCSV.df_petData

    print(df_petData)
    for idx, row in df_petData.iterrows():
        row.legal_code
        if row.legal_code in l_code:
            df_petData.loc[idx, 'legal_code'] = l_code[row.legal_code]
        else:
            # print(legal_code)
            cursor.execute("select legal_code from region_info where name=%s", (row.legal_code))
            a = cursor.fetchone()

            if a is not None:
                s = a[0]
                df_petData.loc[idx, 'legal_code'] = s
            else:
                print(row.legal_code)

        #print(df_petData.loc[idx])

    #print(df_petData)
    df_petData = df_petData.astype(object).where(pd.notnull(df_petData), 0)

    df_petData.to_sql(con=engine, if_exists="append", index=False, name='pet_data')

    print("%s done" % insertPetData.__name__)


# insertRegionInfo()
# insertHospital()
insertAbandonedAnimal()
insertPetData()

cursor.close()
conn.close()
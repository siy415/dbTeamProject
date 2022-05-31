from dataclasses import dataclass
from lib2to3.pgen2.token import EQUAL
import string
import requests
import xml.etree.ElementTree as ET
from urllib.parse import unquote, quote, quote_plus, urlencode
from bs4 import BeautifulSoup as bs
import pandas as pd

api_key = '58bb2b6449dec2d615750219cb8391a4f42efb1f7e16ad63bb45f73f57ef201c'

# 공공데이터에서 반려동물 등록 데이터 파싱

params = {
    'LVSTCK_KND': "고양이",
}

def getResponse ():
    service = "Grid_20210806000000000612_1"

    curCnt = 1
    nextCnt = 1000

    kinds = ["개","고양이"]

    dataFrame = pd.DataFrame()

    for kind in kinds:
        curCnt = 1
        nextCnt = 1000

        url = 'http://211.237.50.150:7080/openapi/' + api_key + "/json/" + service

        requestUrl = url + '/' + str(curCnt) + '/' +str(nextCnt)

        params["LVSTCK_KND"] = kind

        response = requests.get(requestUrl, params=params)
        
        j = response.json()
        totalCnt = int(j[service]["totalCnt"])

        print(j[service]["result"]["message"])

        url = url.replace("json", "xml")

        print(totalCnt)

        while nextCnt < totalCnt:
            requestUrl = url + '/' + str(curCnt) + '/' +str(nextCnt)
            response = requests.get(requestUrl, params=params)

            df = pd.read_xml(response.url, xpath='.//row')

            dataFrame = pd.concat([dataFrame,df])

            temp = nextCnt
            if nextCnt + 1000 < totalCnt:
                nextCnt = nextCnt + 1000
            else:
                nextCnt = totalCnt
            curCnt = temp + 1
            print(nextCnt)

    print(dataFrame)

    dataFrame.to_csv("../csv/petData.csv", encoding='utf-8-sig')


getResponse()
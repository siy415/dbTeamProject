from codecs import getreader
from lib2to3.pgen2.token import EQUAL
from socket import getnameinfo
import string
import requests
import xml.etree.ElementTree as ET
from urllib.parse import unquote, quote, quote_plus, urlencode
from bs4 import BeautifulSoup as bs
import pandas as pd

service = {
    "sido" : "sido",
    "abandon" : "abandonmentPublic",
}

# 공공데이터에서 유기동물 등록 데이터 파싱

api_key = '8EEsivQoU%2FF5gXtfrGxgoDUWv0TNSMcA6SK7TM2DJVyXCyoFescaNQMTQYvf2jYsGeFZcRyPkZanZTy6qd1HEw%3D%3D'
api_key_decode = requests.utils.unquote(api_key)    
params ={'ServiceKey' : api_key_decode}

def getResponse (svs: string, params: dict):
    url = '	http://openapi.animal.go.kr/openapi/service/rest/abandonmentPublicSrvc/' + service[svs]

    response = requests.get(url, params=params)


    # print(response.url)
    # print(response.text)
    contene_decode = quote(response.text)
    #print(contene_decode)

    # soup = bs(response.text, "lxml-xml")
    df = pd.read_xml(response.url, xpath='.//item')

    return df

def getSidoData():
    _params = params
    soup = getResponse("sido", _params)

    return soup

def getAbandonData(bgData: string, endDate: string, regions: list):
    print(" ")

    dogCat_list = ['417000', '422400']      # dog: 417000, cat: 422400

    df_list = []

    _params = {
        'bgnde': bgData,
        'endde': endDate,
        'pageNo': '1',
        'numOfRows': '100000'
    }

    drop_list = ['noticeSdt', 'popfile', 'sexCd', 'specialMark', 'weight', 'careNm' , 'careTel', 'colorCd', 'filename', 'noticeNo', 'processState', 'age', 'noticeComment', 'officetel', 'happenPlace', 'noticeEdt', 'careAddr', 'neuterYn', 'chargeNm'] # happenDt

    for animal in dogCat_list:
        _params['upkind'] = animal
        #for region in regions:
        #    _params['upr_cd'] = region
        
        _params.update(params)

        df_ = getResponse("abandon", _params)

        # df_ = xmlToDataFrame(soup)

        df_list.append(df_)

    # for d in df_list:
    #    d.set_index('desertionNo', inplace=True)

    df = pd.merge(df_list[0], df_list[1], how='outer')
    df.drop(drop_list, axis='columns', inplace=True)

    print(df)

    df.to_csv("test.csv", encoding='utf-8-sig')


def xmlToDataFrame(soup: bs):
    row_list = []
    name_list = []
    value_list = []

    rows = soup.find_all('item')

    for i in range(0, len(rows)):
        cols = rows[i].find_all()
        # print(cols)
        # print(len(cols[i]))
        for j in range(0, len(cols)):
            if i == 0 and cols[j].name != "noticeComment":
                name_list.append(cols[j].name)
                # print(cols[j].name)

            if (cols[j].name != "noticeComment"):
                value_list.append(cols[j].text)
        row_list.append(value_list)
        value_list = []

    # print(name_list)
    # print(row_list)

    df = pd.DataFrame(row_list, columns=name_list)

    # print(df)

    return df


'''
soup = getSidoData()

rows = soup.find_all('item')

row_list = []
name_list = []
value_list = []

for i in range(0, len(rows)):
    cols = rows[i].find_all()
    for j in range(0, len(cols)):
        if i == 0:
            name_list.append(cols[j].name)
        value_list.append(cols[j].text)
    row_list.append(value_list)
    value_list = []
'''

# sido_df = pd.DataFrame(row_list, columns=name_list)
sido_df = getSidoData()


# print(list(sido_df.iloc[:, 0]))


# element = soup.select()

getAbandonData("20210101", "20211231", list(sido_df.iloc[:, 0]))
from base64 import decode
from matplotlib.font_manager import json_load
import pandas as pd
import folium
import webbrowser
import pymysql
from sqlalchemy import create_engine
import json
 
# Load the shape of the zone (US states)
# Find the original file here: https://github.com/python-visualization/folium/tree/master/examples/data
# You have to download this file and set the directory where you saved it
aaa = 'C:\\Users\\siy41\\Desktop\과제\\04_목_db\\팀프\\project\\map\\TL_SCCO_SIG_WGS84.json'
with open(aaa, 'r', encoding="utf-8") as fp:
    state_geo = json.load(fp)

# print(state_geo)

 
# Load the unemployment value of each state
# Find the original file here: https://github.com/python-visualization/folium/tree/master/examples/data

pymysql.install_as_MySQLdb()

# id: root
# pwd: autoset
# ip: localhost:3306
# database: teamProject
engine = create_engine(f"mysql+mysqldb://{'root'}:{'autoset'}"\
                    f"@{'localhost'}:3306/{'teamProject'}",
                    encoding="utf-8")

# conn = pymysql.connect(host='localhost', user='root', passwd='autoset',charset='utf8',database='teamProject')

# cursur = conn.cursor()

# e = cursur.execute("select * from for_analyze")

state_data = pd.read_sql(con=engine, sql="select * from for_analyze")    # db에서 for_analyze view 전달

 
# Initialize the map:
m = folium.Map(location=[36, 127], tiles="OpenStreetMap", zoom_start=7)
 
# Add the color for the chloropleth:

m.choropleth(
 geo_data=state_geo,
 name='choropleth',
 data=state_data,
 columns=['region_name', 'income_lv'],
 key_on='feature.properties.CTP_KOR_NM',
 fill_color='YlGn',
 fill_opacity=0.7,
 line_opacity=0.5,
 legend_name='income level'
)

folium.LayerControl().add_to(m)
 
# Save to html
m.save('income_lv.html')
# webbrowser.open_new("pet_count.html")'


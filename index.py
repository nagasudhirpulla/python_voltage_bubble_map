"""
folium docs - http://python-visualization.github.io/folium/modules.html#
circle options reference - https://leafletjs.com/reference-1.6.0.html#circle
"""

import pandas as pd
import folium
import datetime as dt
from appConfig import loadAppConfig

# read data as dataframe
dataDf = pd.read_excel('input.xlsx')
appConf = loadAppConfig()

tilesProvider = appConf.get("tilesProvider", None)
mapCenter = appConf.get("mapCenter", [21.437730075416685, 77.255859375])
mapZoom = appConf.get("mapZoom", 6)
geojsonBorderColor = appConf.get("geojsonBorderColor", "gray")
bubbleFactor = appConf.get("bubbleFactor", 75)
bubbleBorderColor = appConf.get("bubbleBorderColor", 75)
bubbleFillColor = appConf.get("bubbleFillColor", "red")
bubbleFillOpacity = appConf.get("bubbleFillOpacity", 0)
bubbleThickness = appConf.get("bubbleThickness", 1)


# initialize a map with center and zoom
dataMap = folium.Map(location=mapCenter,
                     zoom_start=mapZoom, tiles=tilesProvider)


# show borders
# style options - https://leafletjs.com/reference-1.7.1.html#path
bordersStyle = {"fillColor": None,
                'color': geojsonBorderColor,
                'weight': 2,
                'fillOpacity': 0}
bordersLayer = folium.GeoJson(
    data=(open("states_india.geojson", 'r').read()),
    name="Borders",
    style_function=lambda x: bordersStyle)
bordersLayer.add_to(dataMap)

busesLayer = folium.FeatureGroup("Buses")
# iterate through each dataframe row
for i in range(len(dataDf)):
    busId = dataDf.iloc[i]['Bus_Number']
    busName = dataDf.iloc[i]['Bus_Name']
    busVoltage = dataDf.iloc[i]['Voltage']
    radius = busVoltage*bubbleFactor
    bubbleClr = bubbleBorderColor
    popUpStr = '{0}<br>Voltage - {1} kV<br>Bus Id - {2}'.format(
        busName, busVoltage, busId)
    folium.Circle(
        location=[dataDf.iloc[i]['Latitude'], dataDf.iloc[i]['Longitude']],
        popup=folium.Popup(popUpStr, min_width=100, max_width=700),
        radius=float(radius),
        color=bubbleClr,
        weight=bubbleThickness,
        fill=True,
        fill_color=bubbleFillColor,
        fill_opacity=bubbleFillOpacity
    ).add_to(busesLayer)

busesLayer.add_to(dataMap)

# add layer control over the map
folium.LayerControl().add_to(dataMap)

# html to be injected for displaying legend
# legendHtml = '''
#      <div style="position: fixed;
#      bottom: 50px; left: 50px; width: 150px; height: 70px;
#      border:2px solid grey; z-index:9999; font-size:14px;
#      ">&nbsp; Fuel Types <br>
#      &nbsp; <i class="fa fa-circle"
#                   style="color:blue"></i> &nbsp; Wind<br>
#      &nbsp; <i class="fa fa-circle"
#                   style="color:red"></i> &nbsp; Solar<br>
#       </div>
#      '''

# inject html into the map html
# dataMap.get_root().html.add_child(folium.Element(legendHtml))

currentTsMicroSec = int(dt.datetime.timestamp(dt.datetime.now())*(10**6))
# save the map as html file
dataMap.save('output/output_{0}.html'.format(currentTsMicroSec))

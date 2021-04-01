# %% import zip working
import requests, zipfile, io

url = 'https://data.montpellier3m.fr/node/12038/download'
r = requests.get(url)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall()
# read .json files and convert to df
import json 
ComptAr = pd.DataFrame()
for name in location['N° Série futur']:
    data = []
    date = []
    for line in open('MMM_EcoCompt_{}_Archive2020.json'.format(str(name))):
        data.append(json.loads(line)['intensity'])
        date.append(json.loads(line)["dateObserved"])
    if len(data) <= 177:
        ComptAr[name] = data
    else:
        ComptAr[name] = data[-177:]
max_bikes_day = ComptAr.max().max()
min_bikes_day = ComptAr.min().min()
date = date[-177:]
date = [w[:10] for w in date]
ComptAr.index = date
#  import localization bikes compter
import numpy as np
import pandas as pd 
import json 
url_location = 'https://data.montpellier3m.fr/node/12013/download'
location = pd.read_csv(url_location, sep = ",|;|:ι")
location = location[['Nom du compteur', 'Latitude','Longitude','N° Série futur']]
# import API key 
with open('apikey.txt') as f:
    api_key = f.readline()
    f.close

# %% ask date to show

# %% adding markers on gm working 


print('data available between 2020-07-08 and 2020-12-31')
# day = input('Enter date you want to see, (format yyyy-mm-dd)')
import tkinter 
import time
import PIL   
import gmaps
gmaps.configure(api_key ='') #personnal API key
PlaceCom_coordinates = (43.608536, 3.879582)
fig = gmaps.figure(center = PlaceCom_coordinates, zoom_level = 12, display_toolbar = False, map_type = 'SATELLITE')
marker_location =location[['Latitude','Longitude']].values.tolist()
marker_location[5] = [43.626611, 3.895644]
marker_location = pd.DataFrame(marker_location)
for i in range(len(marker_location[0])):
    circle_layer = gmaps.symbol_layer([marker_location.loc[i,:]], fill_color = 'green', stroke_color = 'green', scale = int(round(ComptAr[ComptAr.index == '2020-11-06'].iloc[:,i]/150) + 1))
    # display circles by part of 150 bikes
    fig.add_layer(circle_layer)
markers = gmaps.marker_layer(marker_location)
fig.add_layer(markers)
fig

# %% tkinter window WIP
from tk_html_widgets import HTMLLabel
root = tkinter.Tk()
root.geometry('800x800')
root.mainloop()
# %%
import ipywidgets as widgets
gmaps.configure(api_key ='AIzaSyDy-xM-RHIPiqrDO3KDC4y3IlGdHiEV7BA')
PlaceCom_coordinates = (43.608536, 3.879582)
W = gmaps.figure(center = PlaceCom_coordinates, zoom_level = 12, display_toolbar = False, map_type = 'SATELLITE')
address_box = widgets.Text(description = 'Address: ', disabled = True, layout = {'width': '95%', 'margin': '10px 0 0 0'})
widgets.VBox(W, address_box)

# %% test
gmaps.configure(api_key ='AIzaSyDy-xM-RHIPiqrDO3KDC4y3IlGdHiEV7BA') #personnal API key
PlaceCom_coordinates = (43.608536, 3.879582)
fig = gmaps.figure(center = PlaceCom_coordinates, zoom_level = 12, display_toolbar = False, map_type = 'SATELLITE')
marker_locations =location[['Latitude','Longitude']].values.tolist()
marker_locations[5] = [43.626611, 3.895644]
marker_locations = pd.DataFrame(marker_locations)
circle_layer = gmaps.symbol_layer(marker_locations, fill_color = 'green', stroke_color = 'green', scale = 15)
# display circles by part of 150 bikes
fig.add_layer(circle_layer)
markers = gmaps.marker_layer(marker_locations)
fig.add_layer(markers)
fig

# %%
from IPython.display import display
import ipywidgets as widgets
import numpy as np
import pandas as pd 
import json 
import gmaps
import requests, zipfile, io
gmaps.configure(api_key='')


class AcledExplorer(object):
    """
    Jupyter widget for exploring the ACLED dataset.

    The user uses the slider to choose a year. This renders
    a heatmap of civilian victims in that year.
    """
    def location(self):
        url_location = 'https://data.montpellier3m.fr/node/12013/download'
        location = pd.read_csv(url_location, sep = ",|;|:ι")
        location = location[['Latitude','Longitude']].values.tolist()
        return(location)

    def data(date):
        url = 'https://data.montpellier3m.fr/node/12038/download'
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()
        # read .json files and convert to df
        ComptAr = pd.DataFrame()
        place = location()
        for name in place['N° Série futur']:
            data = []
            date = []
            for line in open('MMM_EcoCompt_{}_Archive2020.json'.format(str(name))):
                data.append(json.loads(line)['intensity'])
                date.append(json.loads(line)["dateObserved"])
                if len(data) <= 177:
                    ComptAr[name] = data
                else:
                    ComptAr[name] = data[-177:]
        date = date[-177:]
        date = [w[:10] for w in date]
        ComptAr.index = date
        return(ComptAr)


    def __init__(self):
        self.marker_locations = [(None, None)]
        self._slider = None
        self._slider2 = None
        title_widget = widgets.HTML(
            '<h4>Visualization bike flux Montpellier, France</h4>'
        )
        place = [[43.6162094554924, 3.8744080066680895],[43.6096992492676, 3.89693999290466],[43.61465, 3.8336],[43.5907, 3.81324], [43.615741799999995, 3.9096322], [43.626611, 3.895644], [43.6266977, 3.8956288],[43.6138841, 3.8684671], [43.57926, 3.93327], [43.578829999999996, 3.93324]]
        map_figure = self._render_map(place)
        control = self._render_control()
        self._container = widgets.VBox([title_widget, control, map_figure])

    def render(self):
        display(self._container)
#############################################################################################
    def on_button_clicked(self, b):
        day = self.FloatSlider1.value
        month = self.FloatSlider2.value
        place = [[43.6162094554924, 3.8744080066680895],[43.6096992492676, 3.89693999290466],[43.61465, 3.8336],[43.5907, 3.81324], [43.615741799999995, 3.9096322], [43.626611, 3.895644], [43.6266977, 3.8956288],[43.6138841, 3.8684671], [43.57926, 3.93327], [43.578829999999996, 3.93324]]
        print("Button clicked.")
        self.markers.markers = [gmaps.Symbol(location= place[1],fill_color = 'green', stroke_color = 'green', scale = 10)]
        
        return self._container

    def _render_control(self):

        """ Render the widgets """

        self.FloatSlider1 = widgets.FloatSlider(
        value = 15,
        min = 1,
        max = 31,
        step = 1,
        description = 'Day',
        disabled = False,
        continuous_update = False,
        orientation = 'horizontal',
        readout = True,
        readout_format = '.0f',
    )
        self.FloatSlider2 = widgets.FloatSlider(
        value = 8,
        min = 7,
        max = 12,
        step = 1,
        description = 'Month',
        disabled = False,
        continuous_update = False,
        orientation = 'horizontal',
        readout = True,
        readout_format = '.0f',
    )
    
        self.button = widgets.Button(
            description="Visualize Date"
        )

        self.button.on_click(self.on_button_clicked)

        controls = widgets.VBox(
        [self.FloatSlider1, self.FloatSlider2, self.button])
        return controls

    def _render_map(self, LatitudeLongitude):
        """ Render the initial map """
        self.marker_locations = LatitudeLongitude
        PlaceCom_coordinates = (43.608536, 3.879582)

        place = [[43.6162094554924, 3.8744080066680895],[43.6096992492676, 3.89693999290466],[43.61465, 3.8336],[43.5907, 3.81324], [43.615741799999995, 3.9096322], [43.626611, 3.895644], [43.6266977, 3.8956288],[43.6138841, 3.8684671], [43.57926, 3.93327], [43.578829999999996, 3.93324]]
        fig = gmaps.figure(center=PlaceCom_coordinates, zoom_level=12)
        for i in range(len(place)):
            # display circles by part of 150 bikes
            self.markers = gmaps.symbol_layer(self.marker_locations, fill_color = 'green', stroke_color = 'green', scale =3)
        staticMarkers = gmaps.marker_layer(place)
        fig.add_layer(staticMarkers)
        fig.add_layer(self.markers)
        return fig


AcledExplorer().render()
# %%

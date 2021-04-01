# %%
from IPython.display import display
import ipywidgets as widgets
import numpy as np
import pandas as pd 
import json 
import gmaps
import requests, zipfile, io
gmaps.configure(api_key='')


class Visualization(object):
    

    def data(self):
        url = 'https://data.montpellier3m.fr/node/12038/download'
        r = requests.get(url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()
        # read .json files and convert to df
        ComptAr = []
        Ncompt = [ 'XTH19101158', 'X2H19070220', 'X2H20042633', 'X2H20042632', 'X2H20063161', 'X2H20063164', 'X2H20063163', 'X2H20063162', 'X2H20042634', 'X2H20042635']
        location = []
        for name in Ncompt:
            data = []
            date = []
            for line in open('MMM_EcoCompt_{}_Archive2020.json'.format(str(name))):
                data.append(json.loads(line)['intensity'])
                date.append(json.loads(line)["dateObserved"])
            data = data[-177:]      
            ComptAr.append(data)
        date = date[-177:]
        return(ComptAr, date)


    def __init__(self):
        self.symbols_locations = [(None, None)]
        self._slider = None
        self._slider2 = None
        title_widget = widgets.HTML(
            '<h3>Visualization bike flux Montpellier, France</h3>'
            '<h4> size of circles growing by part of 150 bikers</h4>'
            '<h5>Inspired by  <a href="https://stackoverflow.com/questions/54857781/update-marker-in-gmaps-jupyter-using-widgets">StackOverFlow</a></h5>'
        )
        place = [[43.6162094554924, 3.8744080066680895],[43.6096992492676, 3.89693999290466],[43.61465, 3.8336],[43.5907, 3.81324], [43.615741799999995, 3.9096322], [43.626611, 3.895644], [43.6266977, 3.8956288],[43.6138841, 3.8684671], [43.57926, 3.93327], [43.578829999999996, 3.93324]]
        map_figure = self._render_map(place)
        control = self._render_control()
        self._container = widgets.VBox([title_widget, control, map_figure])

    def render(self):
        display(self._container)
#############################################################################################
# mybinder
    def on_button_clicked(self):
        day = self.FloatSlider1.value 
        month = self.FloatSlider2.value
        print("Button clicked.")
        day = ('0' + str(day))[-2:] # add 0 artificially 
        month = ('0' + str(month))[-2:]
        place = [[43.6162094554924, 3.8744080066680895],[43.6096992492676, 3.89693999290466],[43.61465, 3.8336],[43.5907, 3.81324], [43.615741799999995, 3.9096322], [43.626611, 3.895644], [43.6266977, 3.8956288],[43.6138841, 3.8684671], [43.57926, 3.93327], [43.578829999999996, 3.93324]]
        Compt, dateofday = self.data()
        nb_bikes = []
        nb_days = sum(np.array(dateofday) < '2020-' + month + '-' + day) # carefull to First 0 index
        for i in range(10):
            nb_bikes.append(Compt[i][nb_days])
        self.Gsymbols.markers[0].scale = 15
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
        self.symbols_locations = LatitudeLongitude
        PlaceCom_coordinates = (43.608536, 3.879582)

        place = [[43.6162094554924, 3.8744080066680895],[43.6096992492676, 3.89693999290466],[43.61465, 3.8336],[43.5907, 3.81324], [43.615741799999995, 3.9096322], [43.626611, 3.895644], [43.6266977, 3.8956288],[43.6138841, 3.8684671], [43.57926, 3.93327], [43.578829999999996, 3.93324]]
        fig = gmaps.figure(center=PlaceCom_coordinates, zoom_level=12)

        self.Gsymbols = gmaps.symbol_layer(self.symbols_locations, fill_color = 'green', stroke_color = 'green', scale = 1)
        staticMarkers = gmaps.marker_layer(place)
        fig.add_layer(self.Gsymbols)
        fig.add_layer(staticMarkers)
        return fig


Visualization().render()
# %% 
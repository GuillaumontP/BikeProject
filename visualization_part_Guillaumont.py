# %% import localization bikes compter
import numpy as np
import pandas as pd 
import json 
url_location = 'https://data.montpellier3m.fr/node/12013/download'
location = pd.read_csv(url_location, sep = ",|;|:ι")
location = location[['Nom du compteur', 'Latitude','Longitude']]
# %% 

url = 'https://data.montpellier3m.fr/node/12001/download'
dataList = []
with open('EcoCompt_33.txt') as f:
    for jsonObj in f:
        dataDict = json.loads(jsonObj)
        dataList.append(dataDict)
        
# %%
from PIL import Image, ImageTk
import numpy as np
import tkinter

var = np.linspace(0,100)
top = tkinter.Tk()
top.geometry('800x800')
scale = tkinter.Scale(top, variable = var, activebackground = 'blue')
label = tkinter.Label(top, text = 'Hello world', )
button = tkinter.Button(top, text = 'reset')
w = tkinter.Canvas(top, bg="white", height=400, width=400)
for i in range(len(location['Latitude'])):
    x1 = location.iloc[i,1]*5 + 1
    x2 = location.iloc[i,1]*5 - 1 
    y1 = location.iloc[i,2]*10 + 1
    y2 = location.iloc[i,2]*10 - 1
    point = w.create_oval(x1, y1, x2, y2) 
w.pack(pady = 20)

photo = tkinter.PhotoImage(file= "C:\Users\pierr\hmma238\HMMA238\BikeProject\baboon.ppm")
canvas = tkinter.Canvas(top,width=350, height=200)
canvas.create_image(0, 0, image=photo)
canvas.pack()
#image1 = Image.open("C:\Users\pierr\hmma238\HMMA238\BikeProject\IMG-20200627-WA0045.jpg")
#test = ImageTk.PhotoImage(image1)
#button.pack()
#label.pack()
#scale.pack()
top.mainloop()

# %%

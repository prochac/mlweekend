#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import tkinter as Tk
import grequests
import threading
import matplotlib
from matplotlib.figure import Figure
import matplotlib.animation as animation

matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

API_URL = "http://165.227.157.145:8080/api/do_measurement?x={x}"
DEFAULT_START_X = -20
DEFAULT_END_X = 20
DEFAULT_SCALE = 201
DEFAULT_ACCURACY = 10
DEFAULT_DEGREE = 4

root = Tk.Tk()
root.wm_title("Secret mathematical formula")

f = Figure(figsize=(5, 5), dpi=100)
a = f.add_subplot(111)

canvas = FigureCanvasTkAgg(f, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

formula = Tk.StringVar()
w = Tk.Label(root, textvariable=formula)
w.pack()

urls = list()
for x_ in np.linspace(DEFAULT_START_X, DEFAULT_END_X, DEFAULT_SCALE):
    urls.extend([API_URL.format(x=x_)] * DEFAULT_ACCURACY)
urls = np.split(np.array(urls), 1)

responses = list()


def get_data(urls_):
    for url_batch in np.split(np.array(urls_), 10):
        rs = (grequests.get(u) for u in url_batch)
        response = [
            (res.json()["data"]["x"], res.json()["data"]["y"])
            for res in grequests.map(rs)
            if res.json()["data"]["y"] is not None
        ]
        responses.extend(response)
    print("END")


def animate(_):
    if not responses:
        return
    points = np.array(responses)
    x = points[:, 0]
    y = points[:, 1]

    coefficients = np.polyfit(x, y, DEFAULT_DEGREE)
    func = np.poly1d(coefficients)

    x_fit = np.linspace(x[0], x[-1], 50)
    y_fit = func(x_fit)

    a.clear()
    a.plot(x, y, 'o', x_fit, y_fit)
    formula_ = ""
    for y, x in enumerate(reversed(coefficients)):
        formula_ = "{:+.2f}X^{} ".format(x, y) + formula_
    formula_ = "f(y)=" + formula_
    formula.set(str(formula_))


threading.Thread(target=get_data, args=urls).start()
_ = animation.FuncAnimation(f, animate, interval=1000)
Tk.mainloop()
urls_ = []

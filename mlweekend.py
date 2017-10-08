#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import grequests
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import pylab

matplotlib.use('Agg')

API_URL = "http://165.227.157.145:8080/api/do_measurement?x={x}"
DEFAULT_START_X = -100
DEFAULT_END_X = 100
DEFAULT_SCALE = 101
DEFAULT_ACCURACY = 10
DEFAULT_DEGREE = 4

@click.command()
@click.option('--to-file', 'to_file', type=click.Path(), default="graph.png")
@click.option('--from', 'from_', type=float, prompt='Enter the start of the measurement', default=DEFAULT_START_X)
@click.option('--to', 'to', type=float, prompt='Enter the end of the measurement', default=DEFAULT_END_X)
@click.option('--scale', 'scale', type=int, prompt='Enter the scale (number of measured values)', default=DEFAULT_SCALE)
@click.option('--accuracy', 'accuracy', type=int, prompt='Specify the accuracy (number of repeated measurements)',
              default=DEFAULT_ACCURACY)
@click.option('--degree', 'degree', type=int, prompt='Enter the scale (number of measured values)',
              default=DEFAULT_DEGREE)
def main(from_: int, to: int, scale: int, accuracy: int, degree: int, to_file: str):
    urls = list()

    for x_ in np.linspace(from_, to, scale):
        urls.extend([API_URL.format(x=x_)] * accuracy)

    rs = (grequests.get(u) for u in urls)
    response = [
        (res.json()["data"]["x"], res.json()["data"]["y"])
        for res in grequests.map(rs)
        if res and res.json()["data"]["y"] is not None
    ]

    points = np.array(response)

    x = points[:, 0]
    y = points[:, 1]

    coefficients = np.polyfit(x, y, degree)
    formula = np.poly1d(coefficients)

    print("f(y)=\n", formula)
    with open('formula.txt', 'w') as f:
        f.write(str(formula))

    x_fit = np.linspace(x[0], x[-1], 50)
    y_fit = formula(x_fit)

    fig = plt.figure()
    ax = fig.gca()
    fig.suptitle('Secret mathematical formula')
    plt.xlabel('x')
    plt.ylabel('y')

    ax.plot(x, y, 'o', x_fit, y_fit)
    fig.canvas.draw()
    pylab.savefig(to_file)


if __name__ == '__main__':
    main()

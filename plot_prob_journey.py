import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.animation import FuncAnimation
import json
from typing import Dict

DATA_FOLDER = "prob_distributions_happy"
JSON_FILE = "all_distributions.json"

with open(DATA_FOLDER + "/" + JSON_FILE, 'r') as file:
    data_list = json.load(file)

def dict_to_arr(dis):
    return np.array(list(dis.values()))

def plot_journeys(data: Dict):
    "Create 1 simplex plot for a given distribution"

    words = list(data["dis_with_context"].keys())

    dis_with_context = dict_to_arr(data["dis_with_context"])
    dis_no_context = dict_to_arr(data["dis_no_context"])
    each_cad_dis = data["each_cad_dis"]
    each_dis_with_context = data["each_dis_with_context"]
    each_dis_no_context = data["each_dis_no_context"]
    dola_dis_with_context = dict_to_arr(data["dola_dis_with_context"])
    dola_dis_no_context = dict_to_arr(data["dola_dis_no_context"])
    dola_each_cad_dis = data["dola_each_cad_dis"]

    cad_arr = np.array([list(dis.values()) for dis in list(each_cad_dis.values())])
    dola_cad_arr = np.array([list(dis.values()) for dis in list(dola_each_cad_dis.values())])
    wc_arr = np.array([list(dis.values()) for dis in each_dis_with_context])
    woc_arr = np.array([list(dis.values()) for dis in each_dis_no_context])

    # Set up the 3D plot
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Define the vertices of the simplex (the triangle in 3D space)
    vertices = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    ax.plot_trisurf(vertices[:, 0], vertices[:, 1], vertices[:, 2], color='lightblue', alpha=0.3, edgecolor='gray')

    ax.plot(cad_arr[:, 0], cad_arr[:, 1], cad_arr[:, 2], color='indigo', lw=2, alpha=0.3)
    ax.plot(cad_arr[:, 0], cad_arr[:, 1], cad_arr[:, 2], 'ro', color='indigo', label='CAD', alpha=0.3)

    ax.plot(dola_cad_arr[:, 0], dola_cad_arr[:, 1], dola_cad_arr[:, 2], color='purple', lw=2, alpha=0.3)
    ax.plot(dola_cad_arr[:, 0], dola_cad_arr[:, 1], dola_cad_arr[:, 2], 'ro', color='purple', label='CAD-DoLa', alpha=0.3)

    ax.plot(wc_arr[:, 0], wc_arr[:, 1], wc_arr[:, 2], color='lime', lw=2, alpha=0.3)
    ax.plot(wc_arr[:, 0], wc_arr[:, 1], wc_arr[:, 2], 'ro', color='lime', label='With context', alpha=0.3)

    ax.plot(woc_arr[:, 0], woc_arr[:, 1], woc_arr[:, 2], color='green', lw=2, alpha=0.3)
    ax.plot(woc_arr[:, 0], woc_arr[:, 1], woc_arr[:, 2], 'ro', color='green', label='Without context', alpha=0.3)


    ax.plot([dola_dis_with_context[0]], [dola_dis_with_context[1]], [dola_dis_with_context[2]], 'ro', color='darkred', label='DoLa output with context')
    ax.plot([dola_dis_no_context[0]], [dola_dis_no_context[1]], [dola_dis_no_context[2]], 'ro', color='navy', label='DoLa output without context')

    ax.plot([dis_with_context[0]], [dis_with_context[1]], [dis_with_context[2]], 'ro', color='red', label='Output with context')
    ax.plot([dis_no_context[0]], [dis_no_context[1]], [dis_no_context[2]], 'ro', color='blue', label='Output without context')


    # Set axis limits and labels
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_zlim(0, 1)
    ax.set_xlabel(words[0])
    ax.set_ylabel(words[1])
    ax.set_zlabel(words[2])
    ax.legend()


    ax.view_init(elev=30, azim=45)
    plt.show()

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.animation import FuncAnimation
import json
from typing import Dict, Any

JSON_FILE_PATH = "all_distributions_memotrap/final_data_all_distributions.json"


def dict_to_arr(dis):
    return np.array(list(dis.values()))


def plot_dis_journey(arr, ax, label, color, thin=False):
    if thin:
        lw = 0.9
        arrow_length_ratio = 200
    else:
        lw = 1.8
        arrow_length_ratio = 400
    # Plot the CAD line
    x, y, z = arr[:, 0], arr[:, 1], arr[:, 2]
    dx, dy, dz = np.diff(x), np.diff(y), np.diff(z)

    ax.quiver(
        x[:-1] + dx * 0.999, y[:-1] + dy * 0.999, z[:-1] + dz * 0.999,  # Position near end of each line
        dx * 10, dy * 10, dz * 10,                          # Small vectors for arrowheads
        normalize=True, length=0.0001, arrow_length_ratio=arrow_length_ratio, color=color, lw=lw, label=label
    )
    ax.plot(arr[:, 0], arr[:, 1], arr[:, 2], color=color, lw=lw)


def plot_journeys(data_complex: Dict[str, Any]):
    "Create 1 simplex plot for a given distribution"

    q_num: int = data_complex["num"]
    question: str = data_complex["question"]  # The prompt, excluding any context
    data: Dict = data_complex["all_distributions"]  # The main distributions of interest
    print(q_num)

    words = list(data["dis_with_context"].keys())  # The three words of interest to plot on x, y, z

    dis_with_context = dict_to_arr(data["dis_with_context"])
    dis_no_context = dict_to_arr(data["dis_no_context"])
    dola_dis_with_context = dict_to_arr(data["dola_dis_with_context"])
    dola_dis_no_context = dict_to_arr(data["dola_dis_no_context"])
    
    dola_each_cad_dis: Dict = data["dola_each_cad_dis"]
    each_cad_dis: Dict = data["each_cad_dis"]
    each_dis_with_context: Dict = data["each_dis_with_context"]
    each_dis_no_context: Dict = data["each_dis_no_context"]

    cad_arr = np.array([list(dis.values()) for dis in list(each_cad_dis.values())])
    dola_cad_arr = np.array([list(dis.values()) for dis in list(dola_each_cad_dis.values())])
    wc_arr = np.array([list(dis.values()) for dis in each_dis_with_context])
    woc_arr = np.array([list(dis.values()) for dis in each_dis_no_context])

    # Erroneous: only two words
    if cad_arr.shape[1] != 3:
        return

    # Set up the 3D plot
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Define the vertices of the simplex (the triangle in 3D space)
    vertices = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
    ax.plot_trisurf(vertices[:, 0], vertices[:, 1], vertices[:, 2], color='black', alpha=0.1, zorder=1)
    
    # plot_dis_journey(woc_arr, ax, 'Each layer without context', 'orange', True)
    # plot_dis_journey(wc_arr, ax, 'Each layer with context', 'lime', True)
    
    # plot_dis_journey(cad_arr, ax, 'CAD', 'blue')
    plot_dis_journey(dola_cad_arr, ax, 'CAD-DoLa', 'red')

    ax.plot([dola_dis_with_context[0]], [dola_dis_with_context[1]], [dola_dis_with_context[2]], 'ro', color='darkred')
    ax.plot([dola_dis_no_context[0]], [dola_dis_no_context[1]], [dola_dis_no_context[2]], 'ro', color='darkred')

    # # Plot regular dots with and without context
    # ax.plot([dis_with_context[0]], [dis_with_context[1]], [dis_with_context[2]], 'ro', color='navy')
    # ax.plot([dis_no_context[0]], [dis_no_context[1]], [dis_no_context[2]], 'ro', color='navy')

    # Set axis limits and labels
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_zlim(0, 1)
    ax.set_xlabel(words[0])
    ax.set_ylabel(words[1])
    ax.set_zlabel(words[2])
    ax.legend()
    plt.title(question)

    # Change the view
    ax.view_init(elev=30, azim=45)
    plt.show()


if __name__ == "__main__":
    with open(JSON_FILE_PATH, 'r') as file:
        data_list = json.load(file)

    for data in data_list:
        plot_journeys(data)

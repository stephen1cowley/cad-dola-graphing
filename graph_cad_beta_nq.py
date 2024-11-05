import json
import matplotlib.pyplot as plt
from typing import Dict, List
import os

data_folder: str = 'nq_results_novel'
json_files: List[str] = os.listdir(data_folder)

for json_file in json_files:
    with open(data_folder + "/" + json_file, 'r') as file:
        data: Dict[str, int] = json.load(file)

    print(data)

    x: List[float] = []
    y: List[float] = []

    for key in data:
        x.append(float(key))
        y.append(data[key] * 100 / 2773)

    file_name: str = json_file.split(".")[0]
    layers: str = file_name.split("_")[-2] + " " + file_name.split("_")[-1]
    plt.plot(x, y, label=layers)

plt.xlabel("coefficient")
plt.ylabel("Recall /%")
plt.legend()
plt.title("CAD-DoLa Natural Questions Accuracy")
plt.grid()
plt.show()

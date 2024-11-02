import json
import matplotlib.pyplot as plt
from typing import Dict, List
import os

data_folder: str = 'results_novel_2'
json_files: List[str] = os.listdir(data_folder)

for json_file in json_files:
    with open(data_folder + "/" + json_file, 'r') as file:
        data: Dict[str, int] = json.load(file)

    print(data)

    x: List[float] = []
    y: List[float] = []

    for key in data:
        x.append(float(key))
        y.append(data[key] * 100 / 860)

    file_name: str = json_file.split(".")[0]
    layers: str = file_name.split("_")[-2] + " " + file_name.split("_")[-1]
    plt.plot(x, y, label=layers)

plt.xlabel("log coefficient")
plt.ylabel("EM /%")
plt.legend()
plt.title("Additive CAD-DoLa Memotrap Accuracy")
plt.grid()
plt.show()

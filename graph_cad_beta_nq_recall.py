import json
import matplotlib.pyplot as plt
from typing import Dict, List
import os

data_folder: str = 'experiment_configs/novel-granular/corresponding-results'
json_files: List[str] = os.listdir(data_folder)

for json_file_name in json_files:
    with open(data_folder + "/" + json_file_name, 'r') as file:
        data: Dict[str, Dict[str, int]] = json.load(file)

    print(data)
    recall_data = data["Recall"]

    x: List[float] = []
    y: List[float] = []

    for key in recall_data:
        x.append(float(key))
        y.append(recall_data[key] * 100 / 2773)

    plt.plot(x, y, label=json_file_name.split(".")[0])

plt.xlabel("log coefficient")
plt.ylabel("Recall /%")
plt.legend()
plt.title("Additive-CAD Natural Questions Accuracy")
plt.grid()
plt.show()

import json
import matplotlib.pyplot as plt
from typing import Dict, List

json_files: List[str] = [
    'cad_dola_None_None.json',
]

for json_file in json_files:
    with open(json_file, 'r') as file:
        data: Dict[str, int] = json.load(file)

    print(data)

    x: List[float] = []
    y: List[float] = []

    for key in data:
        x.append(float(key))
        y.append(data[key] * 100 / 860)

    file_name: str = json_file.split(".")[0]
    layers: str = file_name.split("_")[2] + " " + file_name.split("_")[3]
    plt.plot(x, y, label=layers)

plt.xlabel("coefficient")
plt.ylabel("EM /%")
plt.title("LLaMA-7B CAD Memotrap Accuracy")
plt.grid()
plt.show()

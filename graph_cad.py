import json
import matplotlib.pyplot as plt
from typing import Dict, List

json_files: List[str] = [
    'nqswap_results/exp_nqswap.json',
]

for json_file in json_files:
    with open(json_file, 'r') as file:
        data: Dict = json.load(file)

        # For the new format:
        data = data["Recall"]

    print(data)

    x: List[float] = []
    y: List[float] = []

    for key in data:
        x.append(float(key))
        y.append(data[key] * 100 / 3999)

    file_name: str = json_file.split(".")[0]
    # layers: str = file_name.split("_")[2] + " " + file_name.split("_")[3]
    # plt.ylim(bottom=0)
    # plt.ylim(top=42)
    plt.plot(x, y)


plt.xlabel("coefficient")
plt.ylabel("Recall /%")
plt.title("LLaMA-13B CAD Natural Questions Swap Accuracy")
plt.grid()
plt.show()

from typing import Dict, List
import json

# num_questions: int = 2773
# files: List[str] = [
#     'nq_results/nq_cad_dola_None_None.json',
#     'nq_results/nq_cad_dola_low_None.json',
#     'nq_results/nq_cad_dola_None_low.json',
#     'nq_results/nq_cad_dola_low_low.json',
# ]
# result_name: str = 'nq_caddola.json'

num_questions: int = 860
files: List[str] = [
    'results/cad_dola_None_None.json',
    'results/cad_dola_low_None.json',
    'results/cad_dola_None_low.json',
    'results/cad_dola_low_low.json',
]
result_name: str = 'memotrap_caddola.json'

with open(files[0], 'r') as f:
    data_0: Dict[str, int] = json.load(f)

with open(files[1], 'r') as f:
    data_1: Dict[str, int] = json.load(f)

with open(files[2], 'r') as f:
    data_2: Dict[str, int] = json.load(f)

with open(files[3], 'r') as f:
    data_3: Dict[str, int] = json.load(f)


def convert_old_to_new_format(
    datas: List[Dict[str, int]]
) -> Dict[str, Dict[str, Dict[str, List[int]]]]:
    new_data = {"1": {"1": {}, "2": {}, "3": {}, "4": {}}}
    for i in range(len(datas)):
        for key, value in datas[i].items():
            new_data["1"][str(i + 1)][key] = [value, num_questions]
    return new_data


new_data = convert_old_to_new_format([data_0, data_1, data_2, data_3])

with open(f'new_results_format/{result_name}', 'w') as f:
    json.dump(new_data, f)

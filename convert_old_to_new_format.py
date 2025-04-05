from typing import Dict, List
import json

num_questions: int = 2773
# num_questions: int = 860

with open('nq_results/nq_cad_dola_None_None.json', 'r') as f:
# with open('results/cad_dola_None_None.json', 'r') as f:
    data: Dict[str, int] = json.load(f)


def convert_old_to_new_format(
    data: Dict[str, int]
) -> Dict[str, Dict[str, Dict[str, List[int]]]]:
    new_data = {"1": {"1": {}}}
    for key, value in data.items():
        new_data["1"]["1"][key] = [value, num_questions]
    return new_data


new_data = convert_old_to_new_format(data)

with open('new_results_format/nq_cad.json', 'w') as f:
    json.dump(new_data, f)

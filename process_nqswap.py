from typing import Dict, List, Any
import json

my_nqswap: List[Dict] = []

with open('nqswap/nqswap_terrible.jsonl', 'r') as file:
    isq = False
    for line in file:
        line = line.strip()

        dataline: Dict[str, Any] = json.loads(line)

        if isq:
            my_nqswap[-1]["question"] = dataline["context_string"]

        else:
            my_nqswap.append({
                "context": dataline["context_string"],
                "answer": [dataline["gold_answers"]]
            })
        isq = not isq

with open("nqswap.json", 'w') as jf:
    json.dump(my_nqswap, jf)

import json

outjson = "dict_samples.json"
with open(outjson, 'r') as json_input:
    json_out = json.load(json_input)

for key in json_out["ZJetsToNuNu_2024"]:
    sample_dict = json_out["ZJetsToNuNu_2024"][key]
    for string,num in zip(sample_dict["strings"], sample_dict["ntot"]):
        if num == None:
            print(f"To remove {string} run:")
            print(f"davix-rm -E /tmp/x509up_u180940 --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates {string}")
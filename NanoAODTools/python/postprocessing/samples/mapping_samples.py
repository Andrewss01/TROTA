from PhysicsTools.NanoAODTools.postprocessing.samples.samples import *
import optparse
import os
import json

usage = 'python mapping_samples.py'
parser = optparse.OptionParser(usage)
parser.add_option('-x', '--xsec', dest = 'xsec', default = False, action = 'store_true', help = 'Default do not xsec mapping')
parser.add_option('-n', '--nevents', dest = 'nevents', default = False, action = 'store_true', help = 'Default do not nevents mapping')
parser.add_option('-d', '--dictSample', dest = 'dictSample', default = False, action = 'store_true', help = 'Default do not dictSamples file')
parser.add_option('-s', '--stringSample', dest = 'stringSample', default = False, action = 'store_true', help = 'Default do not stringSamples file')
(opt, args) = parser.parse_args()

def get_files_string(sample):
    folder_files = "../../../crab/macros/files/"
    if os.path.exists(folder_files+sample.label+".txt"):
        infile_string = open(folder_files+sample.label+".txt")
        strings = infile_string.readlines()
    else:
        strings = [""]
    return strings

def calculate_nevents(sample):
    strings = get_files_string(sample)
    nevents = 0
    for f in strings:
        if f != "":
            ifile = ROOT.TFile.Open(f)
            h_genweight = ROOT.TH1F(ifile.Get("plots/h_genweight"))
            nevents += h_genweight.GetBinContent(1)
            ifile.Close()
        else:
            nevents = 0
    return nevents
if opt.xsec:
    map_xsec = open("./map_xsec.txt", "w")
    map_xsec.write("unordered_map<int,float> xsecs({\n")
if opt.nevents:
    map_nevents = open("./map_nevents.txt", "w")
    map_nevents.write("unordered_map<int,float> nevents({\n")
if opt.dictSample:
    data = {}
if opt.stringSample:
    string = {}
for d in sample_dict.keys():
    if hasattr(sample_dict[d], "components") or not hasattr(sample_dict[d], "unix_code"):
        continue
    if opt.xsec:
        map_xsec.write("{"+str(sample_dict[d].unix_code)+", "+str(sample_dict[d].sigma)+"},\n")
    if opt.nevents:
        nevents = calculate_nevents(sample_dict[d])
        map_nevents.write("{"+str(sample_dict[d].unix_code)+", "+str(nevents)+"},\n")
    if opt.dictSample:
        data[sample_dict[d].label] = sample_dict[d].unix_code
    if opt.stringSample:
        string[sample_dict[d].label] = get_files_string(sample_dict[d])
    # print(sample_dict[d].label, sample_dict[d].unix_code)
if opt.xsec: 
    map_xsec.write("});")
    map_xsec.close()
if opt.nevents:
    map_nevents.write("});")
    map_nevents.close()
if opt.dictSample:
    json_data = json.dumps(data, indent = 1)
    # write JSON data to file
    with open("dictSample.json", "w") as f:
        f.write(json_data)
if opt.stringSample:
    json_string = json.dumps(string, indent = 1)
    with open("stringSample.json", "w") as f:
        f.write(json_string)
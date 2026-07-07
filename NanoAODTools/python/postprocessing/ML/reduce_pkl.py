# import numpy as np
seed_value= 0
import os
os.environ['PYTHONHASHSEED']=str(seed_value)
import random
random.seed(seed_value)
import numpy as np
np.random.seed(seed_value)
import os
import sys
import pickle as pkl
import ROOT
import json
import argparse
from tqdm import tqdm


ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

# Parse the arguments
parser = argparse.ArgumentParser()
parser.add_argument("-a", "--all", dest="all", action="store_true", default=False)
parser.add_argument("-f", "--folder", dest="folder", default= "/eos/user/a/apuglia/TROTA/TROTA2024/pkls/training_dataset_1_pt_cut_600.pkl")
parser.add_argument("-o", "--outfolder", dest="outfolder", default="/eos/user/a/apuglia/TROTA/TROTA2024/pkls")
args   = parser.parse_args()
all    = args.all
folder = args.folder
outfolder = args.outfolder

# inFile = folder+"/training_dataset_1_pt_cut_600.pkl"
if not os.path.exists(outfolder):
    os.makedirs(outfolder)

if all: 
    for dir in tqdm(os.listdir(folder)): 
        if os.path.isdir(folder+"/"+dir):
            for file in os.listdir(folder+"/"+dir):
                print("file is: ", folder+"/"+dir+"/"+file)
                inFile = folder+"/"+dir+"/"+file
                with open(inFile,'rb') as fpkl:
                    dataset = pkl.load(fpkl)
                components = dataset.keys()
                categories = [ '3j0fj','2j1fj','3j1fj'] 
                print(f'components: {components}')

                for c in components:
                    for cat in categories: 
                        idx_truetop  = [i for i,x in enumerate(dataset[c][cat][3] == 1) if x == True]
                        idx_falsetop = [i for i,x in enumerate(dataset[c][cat][3] == 0) if x == True]

                        print('selezionando i top per: ', c, ' ', cat)
                        print('False tops: ', len(idx_falsetop), ' True tops: ', len(idx_truetop))

                        if len(idx_truetop) == 0:
                            print('NO TRUE TOPS')
                            idx_todrop = random.sample(idx_falsetop, int(len(idx_falsetop)*(0.5)))

                        elif len(idx_falsetop)>len(idx_truetop):
                            idx_todrop = random.sample(idx_falsetop, len(idx_falsetop)-len(idx_truetop))
                        else:
                            idx_todrop = []

                        dataset[c][cat][0] = np.delete(dataset[c][cat][0], idx_todrop, axis = 0)
                        dataset[c][cat][1] = np.delete(dataset[c][cat][1], idx_todrop, axis = 0)
                        dataset[c][cat][2] = np.delete(dataset[c][cat][2], idx_todrop, axis = 0)
                        dataset[c][cat][3] = np.delete(dataset[c][cat][3], idx_todrop, axis = 0)
                        # dataset[c][cat][4] = np.delete(dataset[c][cat][4], idx_todrop, axis = 0)
                        # dataset[c][cat][5] = np.delete(dataset[c][cat][5], idx_todrop, axis = 0)

                        idx_truetop  = [i for i,x in enumerate(dataset[c][cat][3]==1) if x == True]
                        idx_falsetop = [i for i,x in enumerate(dataset[c][cat][3]==0) if x == True]

                        print('selezionando i top per: ', c, ' ', cat)
                        print('False tops: ', len(idx_falsetop), ' True tops: ', len(idx_truetop))

                path_to_pkl = outfolder +"/"+file.replace(".pkl", "_reduced.pkl")

                if path_to_pkl is not None:
                    print(path_to_pkl)
                with open(path_to_pkl, "wb") as f:
                    pkl.dump(dataset, f)
else:
    infile = folder
    with open(infile,'rb') as fpkl:
        dataset = pkl.load(fpkl)
    components = dataset.keys()
    categories = [ '3j0fj','2j1fj','3j1fj'] 
    print(f'components: {components}')

    for c in components:
        for cat in categories: 
            idx_truetop  = [i for i,x in enumerate(dataset[c][cat][3] == 1) if x == True]
            idx_falsetop = [i for i,x in enumerate(dataset[c][cat][3] == 0) if x == True]

            print('selezionando i top per: ', c, ' ', cat)
            print('False tops: ', len(idx_falsetop), ' True tops: ', len(idx_truetop))

            if len(idx_truetop) == 0:
                print('NO TRUE TOPS')
                idx_todrop = random.sample(idx_falsetop, int(len(idx_falsetop)*(0.9)))
                #0.7 per trota2022 0.8 per trota2024

            elif len(idx_falsetop)>2*len(idx_truetop):
                idx_todrop = random.sample(idx_falsetop, len(idx_falsetop)- 2* len(idx_truetop))
                #commentare questo per i 2022
            elif len(idx_falsetop) > len(idx_truetop):
                idx_todrop = random.sample(idx_falsetop, len(idx_falsetop)-  len(idx_truetop))
            else:
                idx_todrop = []

            dataset[c][cat][0] = np.delete(dataset[c][cat][0], idx_todrop, axis = 0)
            dataset[c][cat][1] = np.delete(dataset[c][cat][1], idx_todrop, axis = 0)
            dataset[c][cat][2] = np.delete(dataset[c][cat][2], idx_todrop, axis = 0)
            dataset[c][cat][3] = np.delete(dataset[c][cat][3], idx_todrop, axis = 0)
            # dataset[c][cat][4] = np.delete(dataset[c][cat][4], idx_todrop, axis = 0)
            # dataset[c][cat][5] = np.delete(dataset[c][cat][5], idx_todrop, axis = 0)

            idx_truetop  = [i for i,x in enumerate(dataset[c][cat][3]==1) if x == True]
            idx_falsetop = [i for i,x in enumerate(dataset[c][cat][3]==0) if x == True]

            print('selezionando i top per: ', c, ' ', cat)
            print('False tops: ', len(idx_falsetop), ' True tops: ', len(idx_truetop))

    path_to_pkl = infile.replace(".pkl", "_reduced.pkl")

    if path_to_pkl is not None:
        print(path_to_pkl)
    with open(path_to_pkl, "wb") as f:
        pkl.dump(dataset, f)




import os
import pickle as pkl
from tqdm import tqdm
import argparse

# Parse the arguments
#parser = argparse.ArgumentParser()
#parser.add_argument("-y", "--year", dest="year", type=int, default=2022, help="Year of the training")
#args   = parser.parse_args()
#year   = args.year


path_to_training_folder = '/eos/user/a/apuglia/TROTA/TROTA2024/pkls/dataset_reduced'

# path_to_pkl_folder          = "{}/training_dataset_pt_cut_600".format(path_to_training_folder)
dataset                     = {}

for fileName in os.listdir(path_to_training_folder):
    if fileName.endswith(".pkl") and  not(fileName.startswith(".")):
        path_to_pkl_folder = f"{path_to_training_folder}"
        path_to_file = f"{path_to_pkl_folder}/{fileName}"
        print(path_to_file)
        with open(path_to_file, "rb") as f:
            tmp      = pkl.load(f)
        dataset      = dataset|tmp
    else:
        continue


concName             = "training_dataset_1_pt_cut_600.pkl"
path_to_conc         = f"/eos/user/a/apuglia/TROTA/TROTA2024/pkls/{concName}"
with open(path_to_conc, "wb") as f:
    pkl.dump(obj=dataset, file=f)
import os
import pickle as pkl
from tqdm import tqdm
import argparse

# Parse the arguments
#parser = argparse.ArgumentParser()
#parser.add_argument("-y", "--year", dest="year", type=int, default=2022, help="Year of the training")
#args   = parser.parse_args()
#year   = args.year

#if year==2018:
#    path_to_training_folder = "/eos/user/f/fsalerno/framework/MachineLearning/Training_HOTVR_2018_1_new_def"
    # path_to_training_folder = "/eos/user/l/lfavilla/my_framework/MLstudies/Training_year_{}_1".format(year)
#elif year==2022:
#    path_to_training_folder = "/eos/user/f/fsalerno/framework/MachineLearning/Training_PF_2022_1_jets_20_boosted_200_pt"

path_to_training_folder = '/eos/user/a/apuglia/Tprime/pkls'

path_to_pkl_folder          = "{}/training_dataset_pt_cut_600".format(path_to_training_folder)
dataset                     = {}
for fileName in tqdm(os.listdir(path_to_pkl_folder)):
    if fileName.endswith(".pkl") and  not(fileName.startswith(".")):
        path_to_file = f"{path_to_pkl_folder}/{fileName}"
        print(path_to_file)
        with open(path_to_file, "rb") as f:
            tmp      = pkl.load(f)
        dataset      = dataset|tmp
    else:
        continue

# Save the dataset in a single file
concName             = "training_dataset_1_pt_cut_600.pkl"
path_to_conc         = f"{path_to_training_folder}/{concName}"
with open(path_to_conc, "wb") as f:
    pkl.dump(obj=dataset, file=f)
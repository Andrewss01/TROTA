Repository to use Top Reconstruction: an Object Tagger Algorithm training models, for 2022 and 2024 samples. It works using CMSSW and NanoAODTools. 
For more information on NanoAODTools see: https://github.com/CMSNAFW/nanoAOD-tools


## Installation
```bash
cmsrel CMSSW_X_Y_Z
cd CMSSW_X_Y_Z/src
git clone https://github.com/CMSNAFW/TROTA.git PhysicsTools/
scram b -j 10
cmsenv
```
## Evaluate samples with TROTA scores
Four training are avaible on the repository: two for 2024 samples (Top Mixed and Top Resolved) and two for 2022 samples  (Top Mixed and Top Resolved). They use nanoaodsim samples that are listed in NanoAODTools/python/postprocessing/samples/samples.py

Samples are evaluated using a postprocessor script using condor. Then, all the samples are saved on tier 
```bash
cd CMSSW_X_Y_Z/src/PhysicsTools/NanoAODTools/condor/
python3 post_processor_submitter.py -d *dataset_name* -s (submit jobs) -e (if you need to evaluate samples, otherwise it will only create the Top candidates) --tier (to select the tier for the samples saving) --folder (to choose the name of the folder on the tier) 
```
During the running it is possible to check the status with:

```bash
python3 post_processor_submitter.py -d *dataset_name* --status
```

Also, before submitting the jobs it possible to have a dryrun :

```bash
python3 post_processor_submitter.py -d *dataset_name* --dryrun -s -e
```
this will create the post_processor.py in the folder: condor/tmp/post_processing/dataset_name/file_0/ limitating the entries to 100 so it is possible to run it locally to check its functioning.


## Trainings
The training models are listed in condor/training_models.py, only models with a pt cut at 600 GeV in the training are used, but other models could be produced and uploaded.

## Scores
The post processor produce three types of scores (there will be branches in the tree like: TopMixed_TTScore, TopResolved_TTScore etc.. ):
1.  branch TTScore : probability that the top candidate is a true top
2. branch FTScore: probability that the top candidate is a false top (means that the combinatorial recostruction of the jets is wrong)
3. branch QCDScore: probability that the top candidate is reconstructed from qcd jets 

Using this probabilities is possible to define two other scores that distinguish the signal from the two different backgrounds: 

FT_Score = TTScore/(FTScore + TTScore) ,
QCD_Score = TTScore/(QCDScore + TTScore)

_Note: TTScore, FTScore, QCDScore refer to the names of the branches in the tree, actually they represent a probabilty for the three single categories. FT_Score and QCD_Score are scores that distinguish 1vs1 the signal from one of the two backgrounds._ 

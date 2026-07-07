import os

username        = str(os.environ.get("USER"))
inituser        = str(os.environ.get("USER")[0])
uid             = int(os.getuid())
workdir         = "user" if "user" in os.environ.get('PWD') else "work"

######## machine learning models ########
path_to_model_folder        = "%s/src/PhysicsTools/NanoAODTools/models/" % os.environ["CMSSW_BASE"]

TopMixed_2022_TROTA2D_ptcut    = "model_TopMixed_2022_TROTA2D_ptcut.h5"
TopResolved_2022_TROTA2D_ptcut = "model_TopResolved_2022_TROTA2D_ptcut.h5"

TopMixed_2024_TROTA2D_ptcut    = "model_TopMixed_2024_TROTA2D_ptcut.h5"
TopResolved_2024_TROTA2D_ptcut = "model_TopResolved_2024_TROTA2D_ptcut.h5"


models                      = {}

models["TopMixed_2022_TROTA2D_ptcut"]    = TopMixed_2022_TROTA2D_ptcut 
models["TopResolved_2022_TROTA2D_ptcut"] = TopResolved_2022_TROTA2D_ptcut 

models["TopMixed_2024_TROTA2D_ptcut"]          = TopMixed_2024_TROTA2D_ptcut
models["TopResolved_2024_TROTA2D_ptcut"]       = TopResolved_2024_TROTA2D_ptcut








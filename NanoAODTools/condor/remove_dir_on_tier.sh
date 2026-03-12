#!/bin/bash

PROXY="/tmp/x509up_u180940"
CAPATH="/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates"
BASE="davs://webdav.recas.ba.infn.it:8443/cms/store/user/apuglia/Run3Analysis_Tprime/ZJetsToNuNu_2jets_PT600_1J_2022/"
# Step 1: List files
files=$(davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE")

# Step 2: Delete each file
for file in $files; do
    echo "Deleting $BASE/$file"
    davix-rm -E "$PROXY" --capath "$CAPATH" "$BASE/$file"
done

# Step 3: Remove the (now empty) directory
echo "Deleting directory $BASE"
davix-rm -E "$PROXY" --capath "$CAPATH" "$BASE"


##davix-rm -E /tmp/x509up_u180940 --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates davs://webdav.recas.ba.infn.it:8443/cms/store/user/apuglia/TROTA_2024/PostProcessed_samples/ZJetsToNuNu_HT100to200_2024/tree_hadd_0.root
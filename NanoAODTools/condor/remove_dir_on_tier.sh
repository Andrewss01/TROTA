#!/bin/bash

PROXY="/tmp/x509up_u180940"
CAPATH="/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates"
BASE="davs://webdav.recas.ba.infn.it:8443/cms/store/user/apuglia/TROTA2024/Eval_Samples/WtoLNu_4Jets_1J_2024/WtoLNu-4Jets_Bin-1J_TuneCP5_13p6TeV_madgraphMLM-pythia8/WtoLNu_4Jets_1J_2024/260605_215038/0000"


#
#
# 
# 
# 
# d 
# 
# 
#  

#  
#  
#   
#  

# davs://webdav.recas.ba.infn.it:8443/cms/store/user/apuglia/TROTA2024/Eval_Samples/WtoLNu_4Jets_1J_2024/WtoLNu-4Jets_Bin-1J_TuneCP5_13p6TeV_madgraphMLM-pythia8/WtoLNu_4Jets_1J_2024/260605_215038/0002 




delete_recursive() {
    local dir="$1"
    local entries
    entries=$(davix-ls -E "$PROXY" --capath "$CAPATH" "$dir")

    for entry in $entries; do
        local full_path="$dir/$entry"
        # Prova a listare: se funziona è una sottocartella, altrimenti è un file
        if davix-ls -E "$PROXY" --capath "$CAPATH" "$full_path" &>/dev/null; then
            delete_recursive "$full_path"
        else
            echo "Deleting file $full_path"
            davix-rm -E "$PROXY" --capath "$CAPATH" "$full_path"
        fi
    done

    echo "Deleting directory $dir"
    davix-rm -E "$PROXY" --capath "$CAPATH" "$dir"
}

delete_recursive "$BASE"

# Step 1: List files
# files=$(davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE")

# Step 2: Delete each file
# for file in $files; do
#     # echo "Deleting $BASE/$file"
#     davix-rm -E "$PROXY" --capath "$CAPATH" "$BASE/$file"
# done

# Step 3: Remove the (now empty) directory
# echo "Deleting directory $BASE"
# davix-rm -E "$PROXY" --capath "$CAPATH" "$BASE"

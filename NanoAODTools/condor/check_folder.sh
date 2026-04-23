#!/bin/bash
PROXY="/tmp/x509up_u180940"
CAPATH="/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates"
BASE="davs://webdav.recas.ba.infn.it:8443/cms/store/user/apuglia/Run3Analysis_Tprime/Eval_samples/"


# davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE"

davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE"

# # Step 2: Delete each file
# for file in $files; do
#     dirs=$(davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE$file/")
#     echo " file: $file"
#     for dir in $dirs; do
#         echo "inspecting: $BASE$file/$dir/"
#         davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE$file/$dir/" | wc -l
#     done
# done
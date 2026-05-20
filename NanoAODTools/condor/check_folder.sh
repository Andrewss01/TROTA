#!/bin/bash
PROXY="/tmp/x509up_u180940"
CAPATH="/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates"
BASE="davs://webdav.recas.ba.infn.it:8443/cms/store/user/apuglia/TROTA2024/Training_samples/"


files=$(davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE")

# davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE"
for file in $files; do
    echo " file: $file"
    dirs=$(davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE$file/")
    # davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE$file/" 
    
    for dir in $dirs; do
        echo "inspecting: $BASE$file/$dir/"
        davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE$file/$dir/" | wc -l
    done
done

#davix-mkdir -E /tmp/x509up_u180940 --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates davs://webdav.recas.ba.infn.it:8443/cms/store/user/apuglia/TROTA2022
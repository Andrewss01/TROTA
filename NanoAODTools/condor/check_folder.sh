#!/bin/bash
PROXY="/tmp/x509up_u180940"
CAPATH="/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates"
BASE="davs://webdav.recas.ba.infn.it:8443/cms/store/user/apuglia/TROTA2024/Eval_Samples"

files=$(davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE")

# davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE"
for file in $files; do
    echo " file: $file"
    dirs=$(davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE/$file")
    # davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE/$file" 
    
    for dir in $dirs; do
        dirs2=$(davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE/$file/$dir")
        for dir2 in $dirs2; do 
            dirs3=$(davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE/$file/$dir/$dir2")
        
            for dir3 in $dirs3; do
                dirs4=$(davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE/$file/$dir/$dir2/$dir3")
        
                for dir4 in $dirs4; do
                    echo "inspecting: $BASE/$file/$dir/$dir2/$dir3/$dir4 "
                    davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE/$file/$dir/$dir2/$dir3/$dir4" | wc -l
                done
            done
        done
            
    done
done

#davix-mkdir -E /tmp/x509up_u180940 --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates davs://webdav.recas.ba.infn.it:8443/cms/store/user/apuglia/TROTA2022
#!/bin/bash
PROXY="/tmp/x509up_u180940"
CAPATH="/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates"
BASE="davs://webdav.recas.ba.infn.it:8443/cms/store/user/apuglia/TROTA2024/"

davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE" 
# for file in $files; do
#     echo " file: $file"
#     # dirs=$(davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE/$file")
#     davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE/$file" 
#     # echo "dirs: $dirs"

    # for dir in $dirs; do
    #     if davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE/$file/$dir" &>/dev/null; then
    #         dirs2=$(davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE/$file/$dir")
    #         for dir2 in $dirs2; do 
    #             dirs3=$(davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE/$file/$dir/$dir2")
            
    #             for dir3 in $dirs3; do
    #                 dirs4=$(davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE/$file/$dir/$dir2/$dir3")
    #                 n_dirs=$(davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE/$file/$dir/$dir2/$dir3" | wc -l)
    #                 echo "number of dirs: $n_dirs"
                    
    #                 for dir4 in $dirs4; do
    #                     # echo "inspecting: $BASE/$file/$dir/$dir2/$dir3/$dir4 "
    #                     n_files=$(davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE/$file/$dir/$dir2/$dir3/$dir4" | wc -l)
    #                     echo "number of files: $n_files"
    #                 done
    #             done
    #         done
    #     fi
            
    # done
# done

#davix-mkdir -E /tmp/x509up_u180940 --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates davs://webdav.recas.ba.infn.it:8443/cms/store/user/apuglia/TROTA2022

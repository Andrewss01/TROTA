#!/bin/bash
PROXY="/tmp/x509up_u180940"
CAPATH="/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates"
BASE="davs://webdav.recas.ba.infn.it:8443/cms/store/user/apuglia/TROTA2024/Eval_samples/TT_semilep_2024/20260404_202849"


davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE" | wc -l

#davix-ls -E /tmp/x509up_u180940 --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates davs://webdav.recas.ba.infn.it:8443/cms/store/user/apuglia/Run3Analysis_Tprime/PostProcessed_samples

#davix-mkdir -E /tmp/x509up_u180940 --capath /cvmfs/cms.cern.ch/grid/etc/grid-security/certificates davs://webdav.recas.ba.infn.it:8443/cms/store/user/apuglia/TROTA2024/PostProcessed_samples/


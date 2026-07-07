#!/bin/bash
#!/bin/bash

PROXY="/tmp/x509up_u180940"
CAPATH="/cvmfs/cms.cern.ch/grid/etc/grid-security/certificates"
BASE="davs://webdav.recas.ba.infn.it:8443/cms/store/user/apuglia/TROTA2024/Eval_Samples"

# Lista delle cartelle da cancellare (nomi da appendere dopo $BASE)
# FOLDERS=(
#     "ZJetsToNuNu_HT200to400_2024/20260416_131112"
#     "Top_W_plus_4Q_2024/20260420_211249"
#     "Top_W_minus_4Q_2024/20260420_211249"
#     "QCD_HT40to70_2024/20260417_125643"
#     "WtoLNu_4Jets_4J_2024/20260422_174202"
#     "QCD_HT2000_2024/20260417_125643"
#     "Top_W_minus_LNu2Q_2024/20260420_211249"
#     "ZJetsToNuNu_HT400to800_2024/20260422_173410"
#     "QCD_HT1200to1500_2024/20260417_125643"
#     "QCD_HT100to200_2024/20260417_125643"
#     "QCD_HT1500to2000_2024/20260417_125643"
#     "QCD_HT800to1000_2024/20260417_125643"
#     "QCD_HT70to100_2024/20260417_125643"
#     "Top_W_plus_2L2Nu_2024/20260420_211249"
#     "ZJetsToNuNu_HT100to200_2024/20260416_131112"
#     "Top_W_plus_LNu2Q_2024/20260420_211249"
#     "ZJetsToNuNu_HT2500_2024/20260422_173350"
#     "WtoLNu_4Jets_2J_2024/20260428_093853"
#     "QCD_HT1000to1200_2024/20260417_125643"
#     "TT_semilep_2024/20260404_202849"
#     "WtoLNu_4Jets_1J_2024/20260421_114631"
# )



files=$(davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE")


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

# for folder in "${FOLDERS[@]}"; do
#     target="$BASE/$folder"
#     echo "=== Cancellazione di: $target ==="
#     delete_recursive "$target"
# done

# for file in $files; do
#     target="$BASE/$file"
#     echo "=== Cancellazione di: $target ==="
#     delete_recursive "$target"
# done

# echo "=== Completato ==="
# Step 1: List files
# files=$(davix-ls -E "$PROXY" --capath "$CAPATH" "$BASE")

# # Step 2: Delete each file
# for file in $files; do
#     echo "Deleting $BASE/$file"
#     davix-rm -E "$PROXY" --capath "$CAPATH" "$BASE/$file"
# done

# # Step 3: Remove the (now empty) directory
# # echo "Deleting directory $BASE"
davix-rm -E "$PROXY" --capath "$CAPATH" "$BASE"


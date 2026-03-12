import pickle as pkl
import numpy as np
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument('-i', '--inFile', dest='inFile', required=True)
# args = parser.parse_args()

inFile = "/eos/user/a/apuglia/TROTA/pkls/training_dataset_1_pt_cut_600.pkl"
with open(inFile, 'rb') as f:
    dataset = pkl.load(f)

# categories = ['3j0fj']
print(dataset.keys())
# print(len(dataset['TprimeToTZ_600to800_0']['3j1fj']))
# # Raccogli tutto il pfc da tutti i samples e categorie
# pfc_list = []
# for c in dataset.keys():
#     for cat in categories:
#         try:
#             pfc = dataset[c][cat][4]  # shape (N, 20, 9)
#             pfc_list.append(pfc)
#         except (KeyError, TypeError):
#             continue

# X_pfc = np.concatenate(pfc_list, axis=0)  # shape (N_tot, 20, 9)
# print(f"X_pfc shape: {X_pfc.shape}")
# print(f"Numero di sample totali: {X_pfc.shape[0]}")
# print()

# n_features = X_pfc.shape[2]

# # Nomi delle variabili se li conosci, altrimenti indici
# var_names = [f"pfc_{i}" for i in range(n_features)]

# print(f"{'Var':<10} {'Mean':>15} {'Std':>15} {'Min':>15} {'Max':>15} {'NaN':>8} {'Inf':>8} {'|val|>1e6':>12}")
# print("-" * 100)

# for i in range(n_features):
#     col = X_pfc[:, :, i].flatten()  # tutti i valori di quella feature su tutti i PFC e sample
    
#     nan_count = np.sum(np.isnan(col))
#     inf_count = np.sum(np.isinf(col))
    
#     # maschera per valori finiti
#     finite_mask = np.isfinite(col)
#     col_finite = col[finite_mask]
    
#     mean = np.mean(col_finite) if len(col_finite) > 0 else float('nan')
#     std  = np.std(col_finite)  if len(col_finite) > 0 else float('nan')
#     vmin = np.min(col_finite)  if len(col_finite) > 0 else float('nan')
#     vmax = np.max(col_finite)  if len(col_finite) > 0 else float('nan')
#     large_count = np.sum(np.abs(col_finite) > 1e6)

#     print(f"{var_names[i]:<10} {mean:>15.4e} {std:>15.4e} {vmin:>15.4e} {vmax:>15.4e} {nan_count:>8} {inf_count:>8} {large_count:>12}")

# print()
# print("Suggerimento: le variabili con std >> 1e3 o con molti NaN/Inf sono candidate ad essere droppate o scalate con RobustScaler.")
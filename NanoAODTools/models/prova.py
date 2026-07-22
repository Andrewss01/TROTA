
file = "/eos/user/a/apuglia/TROTA/TROTA2024/pkls/training_dataset_1_pt_cut_600_reduced.pkl"


import pickle

with open(file, 'rb') as f:
    data = pickle.load(f)

# for comp, cat_dict in data.items():
#     print("COMPONENTE:", comp)
#     for cat, elem in cat_dict.items():
#         print("  categoria:", cat, "-> tipo:", type(elem), 
#               "len:", len(elem) if hasattr(elem, '__len__') else None)
#         if hasattr(elem, '__len__'):
#             for i, e in enumerate(elem):
#                 print(f"    [{i}] shape:", getattr(e, 'shape', type(e)))
#     break  # solo il primo componente per non stampare troppo

print(data["TT_hadr_0"]["3j1fj"][1][1])
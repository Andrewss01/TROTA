import numpy as np
import optparse
import pickle as pkl
import ROOT
import os

# ──────────────────────────────────────────────────────────────────────────────
# Nomi delle variabili per componente e per anno
# ──────────────────────────────────────────────────────────────────────────────

JET_VARS = {
    "2018": ["area", "btagDeepB",      "deltaEta", "mass", "deltaPhi", "pt", "deltaPhiFatJet", "deltaEtaFatJet"],
    "2022": ["area", "btagDeepFlavB",  "deltaEta", "mass", "deltaPhi", "pt", "deltaPhiFatJet", "deltaEtaFatJet"],
    "2024": ["area", "btagUParTAK4B",  "deltaEta", "mass", "deltaPhi", "pt", "deltaPhiFatJet", "deltaEtaFatJet"],
}

FATJET_VARS = {
    "2018": ["area", "btagDeepB", "deepTagMD_TvsQCD", "deepTagMD_WvsQCD",
             "deepTag_QCD", "deepTag_QCDothers", "deepTag_TvsQCD", "deepTag_WvsQCD",
             "eta", "mass", "phi", "pt"],
    "2022": ["area", "btagDeepB", "particleNetWithMass_TvsQCD", "particleNetWithMass_WvsQCD",
             "particleNet_QCD", "particleNetWithMass_QCD", "particleNet_XbbVsQCD", "particleNet_XqqVsQCD",
             "eta", "mass", "phi", "pt"],
    "2024": ["area", "globalParT3_Xbb", "particleNetWithMass_TvsQCD", "particleNetWithMass_WvsQCD",
             "particleNet_QCD", "particleNetWithMass_QCD", "particleNet_XbbVsQCD", "particleNet_XqqVsQCD",
             "eta", "mass", "phi", "pt",
             "globalParT3_TopbWev", "globalParT3_TopbWmv", "globalParT3_TopbWqq"],
}

TOP_VARS = {
    "3j0fj": ["mass_jets", "mass_top", "pt_top"],
    "2j1fj": ["mass_jets", "mass_top", "pt_top"],
    "3j1fj": ["mass_jets", "mass_top", "pt_top"],
}

# Variabili pt: usate per imporre il range minimo di 800 GeV sul lato destro
PT_VAR_NAMES = {"pt", "pt_top"}

# ──────────────────────────────────────────────────────────────────────────────
# Definizione dei processi: ordine, colori, etichette
# ──────────────────────────────────────────────────────────────────────────────

PROCESSES = ["Signal", "FalseTop", "QCD"]

PROC_STYLE = {
    #             line color           fill alpha
    "Signal":   (ROOT.kRed,           0.25),
    "FalseTop": (ROOT.kBlue,          0.25),
    "QCD":      (ROOT.kGreen+2,       0.25),
    # "ZJets":    (ROOT.kOrange+1,      0.25),
    # "TT_dilep": (ROOT.kCyan+1,      0.25),
}

PROC_LABEL = {
    "Signal":   "Signal (TT true top)",
    "FalseTop": "False Top (TT truth=0)",
    "QCD":      "QCD",
    # "ZJets":    "Z+Jets",
    # "TT_dilep": "TT dileptonic",
}

def classify_sample(sample_name):
    """
    Ritorna:
      'TT'       → TT_hadr o TT_semilep  (va separato via truth in Signal/FalseTop)
      'TT_dilep' → TT dileptonic
      'QCD'      → QCD
      'ZJets'    → Z+Jets
      None       → campione sconosciuto, ignorato
    """
    if "TT_hadr" in sample_name or "TT_semilep" in sample_name or "Tprime" in sample_name:
        return "TT"
    elif "TT_dilep" in sample_name:
        return "TT"
    elif "QCD" in sample_name:
        return "QCD"
    elif "ZJ" in sample_name:
        return "QCD"
    else:
        return None

# ──────────────────────────────────────────────────────────────────────────────
# Accumulo: proc_data[proc][comp][vname] = lista di float
#
# Componenti prodotte:
#   - "jets"         : tutti i jet (j0, j1, j2) accorpati
#   - "fatjet"       : fatjet (invariato)
#   - "top_mixed"    : 3j0fj + 2j1fj + 3j1fj accorpati
#   - "top_resolved" : solo 3j0fj
# ──────────────────────────────────────────────────────────────────────────────

def accumulate(data, categories, year):
    jet_vars    = JET_VARS[year]
    fatjet_vars = FATJET_VARS[year]

    proc_data = {proc: {} for proc in PROCESSES}

    def ensure_keys(proc, comp, var_names):
        if comp not in proc_data[proc]:
            proc_data[proc][comp] = {v: [] for v in var_names}

    def fill_arrays(proc, comp, var_names, arr2d, mask=None):
        """
        arr2d : np.ndarray (n_tops, n_vars)
        mask  : bool array length n_tops; None = prendi tutto
        """
        ensure_keys(proc, comp, var_names)
        rows = arr2d if mask is None else arr2d[mask]
        for vidx, vname in enumerate(var_names):
            if vidx >= rows.shape[1]:
                continue
            proc_data[proc][comp][vname] += list(rows[:, vidx])

    for sample in data.keys():
        proc_type = classify_sample(sample)
        if proc_type is None:
            print(f"  WARN: campione '{sample}' non classificato, ignorato.")
            continue
        print(f"  Elaborazione campione: {sample}  →  {proc_type}")

        for cat in categories:
            if cat not in data[sample]:
                continue

            arr_jet    = np.array(data[sample][cat][0])                    # (n_tops, n_jets, n_jet_vars)
            arr_fatjet = data[sample][cat][1]                              # (n_tops, n_fj_vars) o None
            arr_top    = np.array(data[sample][cat][2])                    # (n_tops, n_top_vars)
            truth      = np.array(data[sample][cat][3]).flatten().astype(int)

            # Per TT: separa Signal (truth=1) e FalseTop (truth=0)
            if proc_type == "TT":
                masks = {
                    "Signal":   truth == 1,
                    "FalseTop": truth == 0,
                }
            else:
                masks = {proc_type: None}

            for proc, mask in masks.items():

                # ── jets: tutti i jet accorpati in "jets" ────────────────────
                if arr_jet.ndim == 3:
                    for jidx in range(arr_jet.shape[1]):
                        jets2d = arr_jet[:, jidx, :]          # (n_tops, n_jet_vars)
                        fill_arrays(proc, "jets", jet_vars, jets2d, mask)

                # ── fatjet ────────────────────────────────────────────────────
                if arr_fatjet is not None:
                    fj = np.array(arr_fatjet)
                    if fj.ndim == 2 and fj.shape[1] > 0:
                        fill_arrays(proc, "fatjet", fatjet_vars, fj, mask)

                # ── top: top_mixed (tutte le categorie) e top_resolved (solo 3j0fj) ──
                top_vnames = TOP_VARS.get(cat, [f"var_{i}" for i in range(arr_top.shape[1])])

                # Sempre in top_mixed
                fill_arrays(proc, "top_mixed", top_vnames, arr_top, mask)

                # Solo 3j0fj in top_resolved
                if cat == "3j0fj":
                    fill_arrays(proc, "top_resolved", top_vnames, arr_top, mask)

    return proc_data

# ──────────────────────────────────────────────────────────────────────────────
# Calcolo dei range con margine del 35% e minimo 800 per le variabili pt
# ──────────────────────────────────────────────────────────────────────────────

RANGE_MARGIN   = 0.35   # 35% di espansione su ciascun lato
PT_MIN_HI      = 800.0  # valore minimo garantito per il bordo destro delle pt

def compute_range(all_finite, vname):
    """
    Calcola (lo, hi) con margine del 35% sul range percentile 0.5–99.5.
    Per le variabili pt impone hi >= PT_MIN_HI.
    """
    lo_raw = float(np.percentile(all_finite, 0.5))
    hi_raw = float(np.percentile(all_finite, 99.5))

    if lo_raw == hi_raw:
        lo_raw -= 1.0
        hi_raw += 1.0

    span = hi_raw - lo_raw
    margin = RANGE_MARGIN * span

    lo = lo_raw - margin
    hi = hi_raw + margin

    # Per le variabili di tipo pt garantiamo il range fino a PT_MIN_HI
    if vname in PT_VAR_NAMES:
        hi = max(hi, PT_MIN_HI)

    return lo, hi

# ──────────────────────────────────────────────────────────────────────────────
# Scrittura ROOT: una directory per componente, un TH1F + TCanvas per variabile
# ──────────────────────────────────────────────────────────────────────────────

def write_root(proc_data, out_path, n_bins=100):
    rfile = ROOT.TFile.Open(out_path, "RECREATE")

    all_comps = sorted(set(
        comp
        for proc in PROCESSES
        for comp in proc_data[proc].keys()
    ))

    for comp in all_comps:
        rfile.mkdir(comp)
        rfile.cd(comp)

        all_vars = sorted(set(
            vname
            for proc in PROCESSES
            for vname in proc_data[proc].get(comp, {}).keys()
        ))

        for vname in all_vars:

            # Valori finiti per ogni processo + range globale
            vals = {}
            for proc in PROCESSES:
                v = np.array(proc_data[proc].get(comp, {}).get(vname, []), dtype=float)
                vals[proc] = v[np.isfinite(v)]

            all_finite = np.concatenate(list(vals.values()))
            if len(all_finite) == 0:
                print(f"  WARN: {comp}/{vname} vuoto in tutti i processi, salto.")
                continue

            lo, hi = compute_range(all_finite, vname)

            # Crea, riempie e normalizza gli istogrammi
            histos = {}
            for proc in PROCESSES:
                hname = f"{comp}_{vname}_{proc}"
                h = ROOT.TH1F(hname, f"{comp} | {vname};{vname};a.u.", n_bins, lo, hi)
                for v in vals[proc]:
                    h.Fill(v)
                # if h.Integral() > 0:
                #     h.Scale(1.0 / h.Integral())
                color, alpha = PROC_STYLE[proc]
                h.SetLineColor(color)
                h.SetLineWidth(2)
                h.SetFillColorAlpha(color, alpha)
                histos[proc] = h

            # Canvas: disegna dal più alto al più basso
            cname  = f"c_{comp}_{vname}"
            canvas = ROOT.TCanvas(cname, cname, 900, 650)
            canvas.SetLeftMargin(0.12)

            procs_sorted = sorted(PROCESSES, key=lambda p: histos[p].GetMaximum(), reverse=True)
            for i, proc in enumerate(procs_sorted):
                histos[proc].Draw("HIST" if i == 0 else "HIST SAME")

            # Legenda con numero di entries prima della normalizzazione
            legend = ROOT.TLegend(0.58, 0.60, 0.92, 0.92)
            legend.SetBorderSize(0)
            legend.SetFillStyle(0)
            for proc in PROCESSES:
                n = len(vals[proc])
                legend.AddEntry(histos[proc], f"{PROC_LABEL[proc]}  (N={n})", "lf")
            legend.Draw()

            for proc in PROCESSES:
                histos[proc].Write()
            canvas.Write()

        rfile.cd()

    rfile.Close()
    print(f"\nFile ROOT scritto in: {out_path}")

# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────

usage = 'python3 variables_studies_pre_training.py [options]'
parser = optparse.OptionParser(usage)
parser.add_option('-y', '--year',     dest='year',     default='2022',
                  help='Anno di presa dati: 2018, 2022, 2024 (default: 2024)')
parser.add_option('-o', '--outdir',   dest='outdir',   default='/eos/user/a/apuglia/TROTA/TROTA2024/studies_training/',
                  help='Directory di output per il file ROOT')
parser.add_option('-n', '--nbins',    dest='nbins',    default=100, type='int',
                  help='Numero di bin degli istogrammi (default: 100)')
(opt, args) = parser.parse_args()

year     = opt.year
outdir   = opt.outdir
n_bins   = opt.nbins

paths_pkl = {
    "2024": "/eos/user/a/apuglia/TROTA/TROTA2024/pkls/training_dataset_1_pt_cut_600_reduced.pkl",
    "2022":  "/eos/user/a/apuglia/TROTA/TROTA2022/pkls/training_dataset_1_pt_cut_600_reduced.pkl"}

categories =  ["3j1fj", "2j1fj", "3j0fj"]

path_pkl = paths_pkl[year]
print(f"Carico pkl: {path_pkl}")
with open(path_pkl, 'rb') as f:
    data = pkl.load(f)

print(f"Campioni trovati: {list(data.keys())}")
print(f"Anno: {year}    |  Categorie: {categories}")

print("\nAccumulo valori per processo...")
proc_data = accumulate(data, categories, year)

# Stampa riepilogo entries per processo (usando pt_top di top_mixed come riferimento)
print("\nEntries accumulate per processo:")
for proc in PROCESSES:
    n = len(proc_data[proc].get("top_mixed", {}).get("pt_top", []))
    print(f"  {PROC_LABEL[proc]:35s}: {n}")

if not os.path.exists(outdir):
    os.makedirs(outdir)

out_root = os.path.join(outdir, f"studies_pre_training_{year}_new.root")
print(f"\nScrivo file ROOT: {out_root}")
write_root(proc_data, out_root, n_bins=n_bins)

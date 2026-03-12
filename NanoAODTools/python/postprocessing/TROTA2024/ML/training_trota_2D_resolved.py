##### FIX SEED #####
seed_value= 1
import os
os.environ['PYTHONHASHSEED']=str(seed_value)

import random
random.seed(seed_value)
import numpy as np
np.random.seed(seed_value)
import keras
import tensorflow as tf
import keras_tuner as kt
import tensorflow as tf
tf.random.set_seed(12345)
session_conf = tf.compat.v1.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)
sess = tf.compat.v1.Session(graph=tf.compat.v1.get_default_graph(), config=session_conf)
from keras import backend as K
K.set_session(sess)



import os
import sys
from curses import keyname
#import tensorflow as tf
#from tensorflow import keras
import keras_tuner as kt
import pickle as pkl
# import random
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score, f1_score, confusion_matrix, auc, roc_curve
from tensorflow.keras.layers import Dense, Dropout, LSTM, concatenate, GRU,Masking, Activation, TimeDistributed, Conv1D, BatchNormalization, MaxPooling1D, Reshape, Flatten, Conv2D, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import plot_model, to_categorical
from tensorflow.keras.backend import sigmoid
from tensorflow.keras import regularizers
#from keras.utils.generic_utils import get_custom_objects
from keras.utils import CustomObjectScope
import matplotlib.pyplot as plt
import ROOT
import json
import mplhep as hep
hep.style.use(hep.style.CMS)
from sklearn.utils import class_weight
import argparse


ROOT.gROOT.SetBatch()
ROOT.gStyle.SetOptStat(0)

usage = 'python3 training_CNN.py -s TT,ZJ -i /eos/user/a/apuglia/thesis/training_dataset/trainingSet_PF_SV_10k.pkl -o True -g ./model_26_04_2025/ -m ./model_26_04_2025/model_26_04_2025.h5 -j ./model_26_04_2025/scores_26_04_2025.json -v True'

parser = argparse.ArgumentParser(usage)
parser.add_argument('-s', '--samples'   , dest = 'samples'   , required = True  )
parser.add_argument('-i', '--inFile'    , dest = 'inFile'    , required = True  )
parser.add_argument('-o', '--multiscore', dest = 'multiscore', required = True  )
parser.add_argument('-m', '--outModel'  , dest = 'outModel'  , required = False, default = './model_prova.h5' )
parser.add_argument('-j', '--outJson'   , dest = 'outJson'   , required = False)
parser.add_argument('-g', '--graphics'  , dest = 'graphics'  , required = False, default= './grafiche/model_prova')
parser.add_argument('-v', '--verbose'   , dest = 'verbose'   , required = False, default = True )
parser.add_argument('-l', '--label'     , dest = 'label'     , required= True  )

args          = parser.parse_args()
samples       = args.samples.split(',')
inFile        = args.inFile
outModel      = args.outModel
path_outJson  = args.outJson
path_graphics = args.graphics
verbose       = args.verbose
multiscore    = args.multiscore
label         = args.label

if not os.path.exists(path_graphics):
    os.makedirs(path_graphics)
    print('Directory ', path_graphics,'created')

with open(inFile,'rb') as fpkl:
    dataset = pkl.load(fpkl)


components = dataset.keys()
categories = ['3j1fj', '3j0fj', '2j1fj']
if verbose:
    print(f'components: {components}')

components_todrop = []
for c in components:
    for cat in categories:
        if dataset[c][cat] == 0 or c not in samples:
            components_todrop.append(c)
            break
for c_todrop in components_todrop:
    dataset.pop(c_todrop)

for c in components:
    for cat in categories: 
        idx_truetop  = [i for i,x in enumerate(dataset[c][cat][3] == 1) if x == True]
        idx_falsetop = [i for i,x in enumerate(dataset[c][cat][3] == 0) if x == True]

        print('selezionando i top per: ', c, ' ', cat)
        print('False tops: ', len(idx_falsetop), ' True tops: ', len(idx_truetop))

        if len(idx_truetop) == 0:
            print('NO TRUE TOPS')
            idx_todrop = random.sample(idx_falsetop, int(len(idx_falsetop)*(0.9)))
        elif len(idx_falsetop)>2*len(idx_truetop):
            idx_todrop = random.sample(idx_falsetop, len(idx_falsetop)-2*len(idx_truetop))
        else:
            idx_todrop = []

        dataset[c][cat][0] = np.delete(dataset[c][cat][0], idx_todrop, axis = 0)
        dataset[c][cat][1] = np.delete(dataset[c][cat][1], idx_todrop, axis = 0)
        dataset[c][cat][2] = np.delete(dataset[c][cat][2], idx_todrop, axis = 0)
        dataset[c][cat][3] = np.delete(dataset[c][cat][3], idx_todrop, axis = 0)
        dataset[c][cat][4] = np.delete(dataset[c][cat][4], idx_todrop, axis = 0)
        # dataset[c][cat][5] = np.delete(dataset[c][cat][5], idx_todrop, axis = 0)
        

        idx_truetop  = [i for i,x in enumerate(dataset[c][cat][3]==1) if x == True]
        idx_falsetop = [i for i,x in enumerate(dataset[c][cat][3]==0) if x == True]

        print('selezionando i top per: ', c, ' ', cat)
        print('False tops: ', len(idx_falsetop), ' True tops: ', len(idx_truetop))

def multi_score(dataset):
    multi_output = []
    for c in samples:
        for cat in categories:
            for j in dataset[c][cat][3]:
                if j == 0 and ('TT' in c or 'tt' in c or 'Tprime' in c):      #False tops : 0 
                    multi_output.append([0])  
                elif j == 1 and ('TT' in c or 'tt' in c):    #True tops : 1
                    multi_output.append([1])
                elif 'ZJ' in c or 'zj' in c or 'QCD' in c:
                    multi_output.append([2])
    y = np.concatenate([multi_output])
    return y


# X_jet                     = np.concatenate([dataset[c][cat][0] for c in samples for cat in categories]) # here we use only the samples selected by the user
# X_fatjet                  = np.concatenate([dataset[c][cat][1] for c in samples for cat in categories]) # here we use only the samples selected by the user
# X_top                     = np.concatenate([dataset[c][cat][2] for c in samples for cat in categories]) # here we use only the samples selected by the user
# X_pfc                     = np.concatenate([dataset[c][cat][4] for c in samples for cat in categories])
# X_sv                      = np.concatenate([dataset[c][cat][5] for c in samples for cat in categories])
# y                         = np.concatenate([dataset[c][cat][3] for c in samples for cat in categories]) # here we use only the samples selected by the user

# print(f"\tX_jet shape:            {X_jet.shape}")
# print(f"\tX_fatjet shape:         {X_fatjet.shape}")
# print(f"\tX_top shape:            {X_top.shape}")
# print(f"\tX_pfc shape:            {X_pfc.shape}")
# print(f"\tX_sv shape:             {X_sv.shape}")
# print(f"\ty shape:                {y.shape}")



class trainer:
    def __init__(self, X_jet, X_fatjet, X_top, X_pfc,  y, best_hyperparameters = None):
        self.X_jet = X_jet
        self.X_fatjet = X_fatjet
        self.X_top = X_top
        self.X_pfc = X_pfc
        # self.X_sv = X_sv
        self.y = y
        self.best_hps = best_hyperparameters

    def split(self, test_size):
        self.X_jet_train, self.X_jet_test, self.X_fatjet_train, self.X_fatjet_test, self.X_top_train, self.X_top_test, self.X_pfc_train, self.X_pfc_test, self.y_train, self.y_test = train_test_split(self.X_jet, self.X_fatjet, self.X_top, 
        self.X_pfc,  self.y, stratify = self.y, shuffle = True, test_size = test_size)

    def model_builder(self, InputShape_Jet, InputShape_Top, InputShape_Pfc):
        print('best hps in model builder is: ', self.best_hps)  

        # fj_inputs = tf.keras.Input(shape = (InputShape_FatJet,),     name = 'fatjet')
        jet_inputs = tf.keras.Input(shape =  InputShape_Jet, name= 'jet')
        top_inputs = tf.keras.Input(shape = (InputShape_Top,),       name = 'top')
        pfc_inputs = tf.keras.Input(shape =  InputShape_Pfc, name = 'pfc')
        print("Jet input: ", jet_inputs)
        print("pfc input: ", pfc_inputs)
        

        x = BatchNormalization()(jet_inputs)
        jet_1 = x[:,0,:]
        jet_2 = x[:,1,:]
        jet_3 = x[:,2,:]
        
        jet1_processed = Dense(units = self.best_hps['j_units'], activation='relu', kernel_initializer = 'he_normal')(jet_1)
        jet2_processed = Dense(units = self.best_hps['j_units'], activation='relu', kernel_initializer = 'he_normal')(jet_2)
        jet3_processed = Dense(units = self.best_hps['j_units'], activation='relu', kernel_initializer = 'he_normal')(jet_3)
    

        x = concatenate([jet1_processed, jet2_processed, jet3_processed])

        # x = keras.layers.Dense(units=self.best_hps['j_units'],
        #                       activation=self.best_hps['j_activation'],
        #                       kernel_initializer= self.best_hps['j_kernel_initializer'])(x)

        w = pfc_inputs[:,:,:4]
        w = BatchNormalization()(pfc_inputs)
        # 
        w = keras.layers.Dense(units = self.best_hps['pfc_units'], activation = 'relu', 
                                kernel_initializer = 'he_normal')(w)
        w = GlobalAveragePooling1D()(w)
                            #   kernel_initializer = pfc_kernel_initializer)(w)
        
       
        print('x is: ', x)
        print('w is: ', w)
    
        # print('z is: ', w)
        # 
        x = concatenate([x,w])

        


        x = Dense(units = self.best_hps['dense_units'], activation = 'relu', kernel_initializer = 'he_normal')(x)
        
        outputs = Dense(3, activation = 'softmax')(x)
        
        # outputs = Dense(3, activation = 'softmax')(x)
        print('best hps are: ', self.best_hps['j_units'],  self.best_hps['pfc_units'] , self.best_hps['dense_units'])
        self.model = tf.keras.Model(inputs = [jet_inputs, top_inputs, pfc_inputs], outputs = outputs)

        optimizer = tf.keras.optimizers.Nadam(learning_rate = self.best_hps['learning_rate'], clipnorm = 1.0)
        loss = tf.keras.losses.SparseCategoricalCrossentropy()
        self.model.compile(optimizer = optimizer, loss = loss, metrics = ['accuracy'])

    def load_model(self, model_to_load):
        self.model = tf.keras.models.load_model(model_to_load)
        return self.model
    
    def callbacks(self):
        early_stop = keras.callbacks.EarlyStopping(monitor="val_accuracy",
                                                   mode="max", # quantity that has to be monitored(to be minimized in this case)
                                                   patience=40, # number of epochs with no improvement after which training will be stopped.
                                                   min_delta=1e-5,
                                                   restore_best_weights=True) # update the model with the best-seen weights

        # Reduce learning rate when a metric has stopped improving
        reduce_LR = keras.callbacks.ReduceLROnPlateau(monitor="val_accuracy",
                                                      mode="max",# quantity that has to be monitored
                                                      min_delta=1e-5,
                                                      factor=0.01, # factor by which LR has to be reduced...
                                                      patience=10, #...after waiting this number of epochs with no improvements on monitored quantity
                                                      min_lr=1e-15) 
        self.callbacks_list = [early_stop]

    def training(self, validation_split, epochs, batch_size, save_model = True, path_to_model = outModel):
        self.callbacks()
        self.model_builder( self.X_jet_train.shape[2], self.X_top_train.shape[1], self.X_pfc_train.shape[2])
        print('model is: ', self.model)
        print('y train is: ', np.unique(self.y_train))
        weights = class_weight.compute_class_weight(class_weight= 'balanced', classes = np.unique(self.y_train), y = np.concatenate(self.y_train))
        class_weights = {0: weights[0], 1: weights[1], 2: weights[2]}
        print('class weights is: ',class_weights)
        self.history = self.model.fit({'jet': self.X_jet_train, 'top': self.X_top_train, 'pfc': self.X_pfc_train}, 
                                      self.y_train, callbacks = self.callbacks_list, validation_split = validation_split, epochs = epochs, batch_size = batch_size, 
                                      verbose = verbose, class_weight = class_weights)
        if save_model:
            self.model.save(path_to_model)

    def predict(self, X_jet_train = None, X_top_train = None, X_pfc_train = None, X_jet_test = None, X_fatjet_test = None, X_top_test = None, X_pfc_test = None):
        if (X_jet_train is None)  and (X_top_train is None) and (X_pfc_train is None):
            self.y_pred_train = self.model.predict({ 'jet': self.X_jet_train, 'top': self.X_top_train, 'pfc': self.X_pfc_train})
            self.y_pred_test  = self.model.predict({  'jet': self.X_jet_test , 'top': self.X_top_test, 'pfc': self.X_pfc_test})
        else:
            y_pred_train = self.model.predict({ 'jet': X_jet_train, 'top': X_top_train, 'pfc': X_pfc_train})
            y_pred_test  = self.model.predict({ 'jet': X_jet_test , 'top': X_top_test, 'pfc': X_pfc_test })
            return y_pred_train, y_pred_test

    def train_test_discrimination(self, bins):
        self.predict()

        y_pred_train_bkg_tt = self.y_pred_train[self.y_train.flatten() == 0, 1]
        y_pred_train_sgn    = self.y_pred_train[self.y_train.flatten() == 1, 1]
        y_pred_train_zj     = self.y_pred_train[self.y_train.flatten() == 2, 1]

        y_pred_test_bkg_tt  = self.y_pred_test[self.y_test.flatten() == 0, 1]
        y_pred_test_sgn     = self.y_pred_test[self.y_test.flatten() == 1, 1]
        y_pred_test_zj      = self.y_pred_test[self.y_test.flatten() == 2, 1]

        train_test_pred = {}
        train_test_pred['train_bkg_ft'] = y_pred_train_bkg_tt
        train_test_pred['train_sgn']    = y_pred_train_sgn
        train_test_pred['train_bkg_qcd'] = y_pred_train_zj
        train_test_pred['test_bkg_ft']  = y_pred_test_bkg_tt
        train_test_pred['test_sgn']     = y_pred_test_sgn
        train_test_pred['test_bkg_qcd']  = y_pred_test_zj

        train_test_histos = {}
        ROOT.gStyle.SetOptStat(0)
        c = ROOT.TCanvas('c','c', 600, 600)
        c.SetLogy()
        c.Draw()
        
        leg = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
        train_test_histos['train_bkg_ft'] = ROOT.TH1F('histo_train_bkg_tt', 'histo_train_bkg_tt', bins, 0, 1)
        train_test_histos['train_sgn'] = ROOT.TH1F('histo_train_sgn', 'histo_train_sgn', bins, 0, 1)
        train_test_histos['train_bkg_qcd'] = ROOT.TH1F('histo_train_bkg_zj', 'histo_train_bkg_zj', bins, 0, 1)
        train_test_histos['test_bkg_ft'] = ROOT.TH1F('histo_test_bkg_tt', 'histo_test_bkg_tt', bins, 0, 1)
        train_test_histos['test_sgn'] = ROOT.TH1F('histo_test_sgn', 'histo_test_sgn', bins, 0, 1)
        train_test_histos['test_bkg_qcd'] = ROOT.TH1F('histo_test_bkg_zj', 'histo_test_bkg_zj', bins, 0, 1)

        for k in train_test_pred.keys():
            for q in train_test_pred[k]:
                train_test_histos[k].Fill(q)

            train_test_histos[k].Scale(1./train_test_histos[k].Integral())
            train_test_histos[k].SetTitle('')
            train_test_histos[k].GetXaxis().SetTitle('Score')
            train_test_histos[k].GetYaxis().SetTitle('Normalized Counts')
            train_test_histos[k].SetMaximum(1)

            if 'test' in k:
                train_test_histos[k].SetMarkerStyle(ROOT.kFullCircle)
                leg.AddEntry(train_test_histos[k], k, 'p')
            elif 'train' in k:
                leg.AddEntry(train_test_histos[k], k, 'f')

        train_test_histos["train_bkg_ft"].SetFillColorAlpha(ROOT.kBlue, 0.3)
        train_test_histos["train_bkg_ft"].SetLineColorAlpha(ROOT.kBlue, 0.3)
        train_test_histos["train_sgn"].SetFillColorAlpha(ROOT.kRed,  0.3)
        train_test_histos["train_sgn"].SetLineColorAlpha(ROOT.kRed,  0.3)
        train_test_histos["train_bkg_qcd"].SetFillColorAlpha(ROOT.kGreen, 0.3)
        train_test_histos["train_bkg_qcd"].SetLineColorAlpha(ROOT.kGreen, 0.3)

        train_test_histos["test_bkg_ft"].SetMarkerColor(ROOT.kBlue)
        train_test_histos["test_sgn"].SetMarkerColor(ROOT.kRed)
        train_test_histos["test_bkg_qcd"].SetMarkerColor(ROOT.kGreen)

        train_test_histos["train_bkg_ft"].Draw("HIST")
        train_test_histos["train_sgn"].Draw("HISTSAME")
        train_test_histos["test_bkg_ft"].Draw("SAME")
        train_test_histos["test_sgn"].Draw("SAME")
        train_test_histos["train_bkg_qcd"].Draw('SAME')
        train_test_histos["test_bkg_qcd"].Draw('SAME')
        leg.Draw("SAME")

        c.SaveAs(f"{path_graphics}/traintestDiscrimination.png")
        c.SaveAs(f"{path_graphics}/traintestDiscrimination.pdf")

    def plot_roc(self, name, labels, predictions, color = 'steelblue', linestyle = '--', roc_model = 'OvR'):
        plt.figure(figsize = (10,7))

        FPR, TPR, TRS = [], [], []
        if roc_model == 'OvR':
            for class_label in [0,1,2]:
                y_ovr_test = np.where(labels == class_label, 1, 0) #mette uno quando abbiamo la classe in questione altrimenti zero 
                y_ovr_pred_test = predictions[:,class_label]    #qua prende le previsioni che corrispondono alla classe in gioco 
                fpr, tpr, trs = roc_curve(y_ovr_test, y_ovr_pred_test)

                #Confronta le previsioni con le vere label. I true positive sono quelli che sono veramente della classe chbe staimo considerando
                #I false positive sono invece quelli che vengono presi come della classe ma sono in realtà delle altre due

                FPR.append(fpr)
                TPR.append(tpr)
                TRS.append(trs)

                plt.plot(fpr, tpr, label = name[class_label], linewidth = 2, color = color[class_label], linestyle = linestyle)

        elif roc_model == 'OvO':
            for class_label in [0,2]:
                p_sig_test = predictions[:,1]
                p_bkg_test = predictions[:, class_label]

                p_sigvsbkg = p_sig_test/(p_sig_test + p_bkg_test)
                p_sigvsbkg_test = np.array([x for x,y in zip(p_sigvsbkg, labels) if y == 1 or y == class_label])

                #si prende questo nuovo score solo per la classe true tops e false top per esempio
                y_sigvsbkg = np.array([x for x in labels if x ==1 or x == class_label])

                #si prendono solo i true e i false tops e per ognuno si considera  1 se sono true top e zero se sono false top.
                #Si confrontano queste label con le probabilità
                y_sigvsbkg_test = np.where(y_sigvsbkg == 1, 1, 0)
                fpr, tpr, trs = roc_curve(y_sigvsbkg_test, p_sigvsbkg_test)

                FPR.append(fpr)
                TPR.append(tpr)
                TRS.append(trs)

                plt.plot(fpr, tpr, label = name[int(class_label/2)], linewidth =2, color = color[class_label], linestyle = linestyle)
                
        plt.xlabel('False positives [%]')
        plt.ylabel('True positives [%]')
        plt.grid(True)

        plt.xscale('log')
        plt.legend(loc = 'lower right')
        
        if roc_model == 'OvR':
            plt.savefig(f"{path_graphics}/roc_curve_OvR.png")
            plt.savefig(f"{path_graphics}/roc_curve_OvR.pdf")
        elif roc_model == 'OvO':
            plt.savefig(f"{path_graphics}/roc_curve_OvO.png")
            plt.savefig(f"{path_graphics}/roc_curve_OvO.pdf")

        return FPR, TPR, TRS

    def test_roc(self, roc_model = 'OvR'):
        if roc_model == 'OvR':
            names_ovr = ['False Top', 'True Top', 'QCD']
            colors = ['steelblue', 'darkorange', 'green']

            fpr_ovr, tpr_ovr, trs_ovr = self.plot_roc(names_ovr, np.concatenate(self.y_test), self.y_pred_test, color = colors, linestyle = '--', roc_model = 'OvR')
            results_ovr = [fpr_ovr, tpr_ovr, trs_ovr]

            return results_ovr
        if roc_model == 'OvO':

            names_ovo = ['True top vs False top', 'True top vs QCD']
            colors = ['steelblue', 'darkorange', 'green']

            fpr_ovo, tpr_ovo, trs_ovo = self.plot_roc(names_ovo, np.concatenate(self.y_test), self.y_pred_test, color = colors, linestyle = '--', roc_model = 'OvO')
            results_ovo = [fpr_ovo, tpr_ovo, trs_ovo]

            return results_ovo

    def evaluate(self, X_jet_test = None, X_fatjet_test = None, X_top_test = None, X_pfc_test = None, y_test = None):

        if (X_jet_test is None) and (X_fatjet_test is None) and (X_top_test is None) and (y_test is None) and (X_pfc_test is None) :
            self.eval_result = self.model.evaluate({ "jet": self.X_jet_test, "top": self.X_top_test, "pfc": self.X_pfc_test}, self.y_test)
            return self.eval_result
        else:
            eval_result      = self.model.evaluate({ "jet": X_jet_test, "top": X_top_test, "pfc": X_pfc_test}, y_test)
            return eval_result



        
X_jet                     = np.concatenate([dataset[c][cat][0] for c in samples for cat in categories]) # here we use only the samples selected by the user
X_fatjet                  = np.concatenate([dataset[c][cat][1] for c in samples for cat in categories]) # here we use only the samples selected by the user
X_top                     = np.concatenate([dataset[c][cat][2] for c in samples for cat in categories]) # here we use only the samples selected by the user
X_pfc                     = np.concatenate([dataset[c][cat][4] for c in samples for cat in categories])
# X_sv                      = np.concatenate([dataset[c][cat][5] for c in samples for cat in categories])
y                         = np.concatenate([dataset[c][cat][3] for c in samples for cat in categories]) # here we use only the samples selected by the user


if multiscore:
    y = multi_score(dataset)
    
data = X_jet, X_fatjet, X_top, X_pfc, y

if verbose:
    print("Data loaded for the training:")
    # print(f"X jet is: {X_jet} ")
    # print(f"X fat jet is: {X_fatjet} ")
    # print(f"X tops is: {X_top} ")
    # print(f"y is: {y} ")
    print(f"\tsamples used:           {samples}")
    print(f"\tNumber of tops:         {len(y)}")
    print(f"\tNumber of true tops:    {len([i for i, x in enumerate(y == 1) if x == True])}")
    print(f"\tNumber of false tops:   {len([i for i, x in enumerate(y == 0) if x == True])}")
    print(f"\tNumber of Z jets:       {len([i for i, x in enumerate(y == 2) if x == True])}")
    print(f"\tX_jet shape:            {X_jet.shape}")
    print(f"\tX_fatjet shape:         {X_fatjet.shape}")
    print(f"\tX_top shape:            {X_top.shape}")
    print(f"\tX_pfc shape:            {X_pfc.shape}")
    # print(f"\tX_sv shape:             {X_sv.shape}")
    print(f"\ty shape:                {y.shape}")


# print('X_pfc is: ', X_pfc[:,:,:3])

best_hps_file = '/afs/cern.ch/user/a/apuglia/CMSSW_14_1_7/src/PhysicsTools/NanoAODTools/python/postprocessing/TROTA_2024/trainings/grid_search_trota_2D_resolved_'+label+'/best_hps_'+label+'.json'
# best_hps_file = 
with open(best_hps_file) as hps_file:
    best_hyperparams = json.load(hps_file)
print(f'BEST HPS ARE: ', best_hyperparams)
trainer1 = trainer(*data,best_hyperparams)
trainer1.split(test_size= 0.4)
trainer1.model_builder( trainer1.X_jet_train.shape[2], trainer1.X_top_train.shape[1], trainer1.X_pfc_train.shape[2])
trainer1.training(validation_split = 0.4, epochs = 5, batch_size = 250, save_model = True, path_to_model = outModel)

best_hps_path = path_outJson.replace('scores', 'best_hps')
with open(best_hps_path, 'w') as jsFile:
    json.dump(best_hyperparams, jsFile, indent = 4)

eval_result = trainer1.evaluate()
trainer1.train_test_discrimination(bins = 100)
ovr_res = trainer1.test_roc(roc_model = 'OvR')
ovo_res = trainer1.test_roc(roc_model = 'OvO')

if verbose:
    for fpr,tpr,trs in zip(ovr_res[0], ovr_res[1], ovr_res[2]):
        print('10%   trs', trs[fpr<0.1][-1], 'tpr ', tpr[fpr<0.1][-1])
        print('5%    trs', trs[fpr<0.05][-1], 'tpr ', tpr[fpr<0.05][-1])
        print('1%    trs', trs[fpr<0.01][-1], 'tpr ', tpr[fpr<0.01][-1])
        print('0.1%  trs', trs[fpr<0.001][-1], 'tpr ', tpr[fpr<0.001][-1])

fprs_wp          = [("10%", 0.1), ("5%", 0.05), ("1%", 0.01), ("0.1%", 0.001)]
components = ["False TT", "True TT", "ZJ"] 
scores = {}
fpr_ovr, tpr_ovr, trs_ovr = ovr_res[0], ovr_res[1], ovr_res[2]
for index in range(len(components)):
    scores[components[index]] = {}
    fpr, tpr, trs = fpr_ovr[index], tpr_ovr[index], trs_ovr[index]
    for wp in fprs_wp:
        scores[components[index]]['fpr ' + wp[0]] = float(fpr[fpr<wp[1]][-1])
        scores[components[index]]['tpr ' + wp[0]] = float(tpr[fpr<wp[1]][-1])
        scores[components[index]]['trs ' + wp[0]] = float(trs[fpr<wp[1]][-1])


components = ['True TT vs False TT', 'True TT vs ZJets']

fpr_ovo, tpr_ovo, trs_ovo = ovo_res[0], ovo_res[1], ovo_res[2]
for index in range(len(components)):
    scores[components[index]] = {}
    fpr, tpr, trs = fpr_ovo[index], tpr_ovo[index], trs_ovo[index]
    for wp in fprs_wp:
        scores[components[index]]['fpr'+wp[0]] = float(fpr[fpr<wp[1]][-1])
        scores[components[index]]['tpr'+wp[0]] = float(tpr[fpr<wp[1]][-1])
        scores[components[index]]['trs'+wp[0]] = float(trs[fpr<wp[1]][-1])

            

with open(path_outJson, "w") as f:
    json.dump(scores, f, indent=4)



metric  = "accuracy"
history = trainer1.history
fig, ax = plt.subplots(ncols=2, figsize=(25,10))
for var in history.history.keys():
    if ("loss" in var) and (not "val" in var): ax[1].plot(history.history[var], label="train")
    if "val_loss" in var: ax[1].plot(history.history[var], label ="val")
    if (f"{metric}" in var) and (not "val" in var): ax[0].plot(history.history[var], label="train")
    if f"val_{metric}" in var : ax[0].plot(history.history[var], label ="val")

ax[0].set_title(f"model {metric}")
ax[0].set_ylabel(f"{metric}")
ax[0].set_xlabel("epoch")
ax[0].legend()
# summarize history for loss
ax[1].set_title("model loss")
ax[1].set_ylabel("loss")
ax[1].set_xlabel("epoch")
ax[1].legend()
ax[1].set_yscale("log")
plt.savefig(f"{path_graphics}/{metric}_loss.png")
plt.savefig(f"{path_graphics}/{metric}_loss.pdf")
print("done")
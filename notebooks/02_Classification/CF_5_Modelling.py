# Custom functions for modelling section

import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt

from sklearn.preprocessing import MinMaxScaler, StandardScaler

from sklearn.model_selection import train_test_split, cross_validate, GridSearchCV

from sklearn.ensemble import RandomForestClassifier

from sklearn.cluster import KMeans

from xgboost import XGBClassifier

from sklearn.feature_selection import SelectKBest, f_classif

from sklearn.metrics import (accuracy_score, balanced_accuracy_score, precision_score, 
                             recall_score, confusion_matrix, plot_confusion_matrix, 
                             make_scorer,multilabel_confusion_matrix,ConfusionMatrixDisplay)

from sklearn.pipeline import make_pipeline, Pipeline

from sklearn.dummy import DummyClassifier

import warnings

def add_model_score(model_score,model,model_name,y_test,y_pred):
    model_score.loc[model_name,'accuracy'] = accuracy_score(y_test,y_pred)    
    model_score.loc[model_name,'balanced accuracy'] = balanced_accuracy_score(y_test,y_pred)
    
    precision_arr = precision_score(y_test,y_pred,average=None,labels=['++','+','-','--'])
    recall_arr = recall_score(y_test,y_pred,average=None,labels=['++','+','-','--'])
    
    precision_arr_weight = precision_score(y_test,y_pred,average='weighted',labels=['++','+','-','--']) 
    recall_arr_weight = recall_score(y_test,y_pred,average='weighted',labels=['++','+','-','--'])
    
    model_score.loc[model_name,'precision avg'] = precision_arr_weight
    model_score.loc[model_name,'recall avg'] = recall_arr_weight
    
    model_score.loc[model_name,'precision (++)'] = precision_arr[0]
    model_score.loc[model_name,'precision (+)'] = precision_arr[1]
    model_score.loc[model_name,'precision (-)'] = precision_arr[2]
    model_score.loc[model_name,'precision (--)'] = precision_arr[3]
    
    model_score.loc[model_name,'recall (++)'] = recall_arr[0]
    model_score.loc[model_name,'recall (+)'] = recall_arr[1]
    model_score.loc[model_name,'recall (-)'] = recall_arr[2]
    model_score.loc[model_name,'recall (--)'] = recall_arr[3]
    
    model_score.loc[model_name,'pos neg class'] = scorer_pos_neg_class(y_test,y_pred)
    
    if ('RFC' in model_name) or ('XGB' in model_name):
        
        if ~('base' in model_name):
            model_score.loc[model_name,'max depth'] = model.best_estimator_.named_steps.model.max_depth
        else:
            model_score.loc[model_name,'max depth'] = np.nan
    else : 
        model_score.loc[model_name,'max depth'] = np.nan
    
    return model_score[model_score.index == model_name]
    
def feat_imp(model,X):
    plt.subplots(figsize=(10, 5))
    imps = model.best_estimator_.named_steps.model.feature_importances_
    rf_feat_imps = pd.Series(imps, index=X.columns).sort_values(ascending=False)
    rf_feat_imps.plot(kind='bar')
    plt.xlabel('Features')
    plt.ylabel('Importance')
    plt.title('Best feature importances');
    
    return plt.show()

def scorer_pos_neg_class(y_test,y_pred):
    mat_conf = confusion_matrix(y_test,y_pred)

    pos_2_neg = mat_conf[[0,1],2:].sum()
    neg_2_pos = mat_conf[[2,3],:2].sum()

    pos_neg_misclass = 1-(pos_2_neg+neg_2_pos)/mat_conf.sum()
    
    return pos_neg_misclass

def scorer_confusion_matrix(y_test,y_pred):
    return confusion_matrix(y_test,y_pred)
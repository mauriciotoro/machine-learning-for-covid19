import pandas as pd
import lightgbm as lgbm
import joblib

lgbm_clf = joblib.load("sigmoid_20200626-110814.pkl")
def calculadora(info):
    
    X_test = pd.DataFrame(info, index=[0])
    orden = ['SEXO', 'NEUMONIA', 'EDAD', 'EMBARAZO', 'DIABETES', 
            'EPOC', 'ASMA', 'INMUSUPR', 'HIPERTENSION', 'OTRA_COM', 
            'CARDIOVASCULAR', 'OBESIDAD', 'RENAL_CRONICA', 'TABAQUISMO']
    X_test = X_test.loc[:,orden]

    categoricas = ['SEXO', 'NEUMONIA', 'EMBARAZO', 'DIABETES', 'EPOC',
        'ASMA', 'INMUSUPR', 'HIPERTENSION', 'OTRA_COM', 'CARDIOVASCULAR',
        'OBESIDAD', 'RENAL_CRONICA', 'TABAQUISMO']
    for col in categoricas:
        X_test[col] = X_test[col].astype('category')

    y_scores = lgbm_clf.predict_proba(X_test)[:,1][0]
    out_dict = {
        "probabilidad": y_scores
    }
    return out_dict

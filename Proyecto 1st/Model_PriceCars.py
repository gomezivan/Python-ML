#!/usr/bin/python

import pandas as pd
from sklearn.externals import joblib
import category_encoders as ce
import sys
import os


def predict_car_value(Make_par, Model_par,State_par,Mileage_par,Year_par):
    #Crear un dataframe y aplicar el encoder binario
    df = pd.DataFrame([{'Year': Year_par, 'Mileage': Mileage_par, 'State':State_par, 'Make':Make_par, 'Model':Model_par}] ) 
    BinEncoder = joblib.load('BinEncoder.pkl') 
    df2 = BinEncoder.transform(df)
    
    rf = joblib.load('RF_modelcars.pkl') 
    value = rf.predict(df2)[0]
    return round(value)



if __name__ == "__main__":
    
    if len(sys.argv) == 1:
        print('Please add an URL')
        
    else:

        url = sys.argv[1]

        p1 = predict_proba(url)
        
        print(url)
        print('Value: ', p1)
        
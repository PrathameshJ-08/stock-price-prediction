import joblib 
import numpy as np
import pandas as pd

def preprocess(Open, High, Low, Volume):
    Open= float(Open)
    High= float(High)
    Low= float(Low)
    Volume= float(Volume)
    # Open = Open
    # High = High.astype(float)
    # Low = Low.astype(float)
    # Volume = Volume.astype(float)


    test_data = [[Open, High, Low, Volume]]
    trained_model = joblib.load('model.pkl')
    prediction = trained_model.predict(test_data)
    return prediction
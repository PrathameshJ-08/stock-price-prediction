import csv
import pandas as pd
import joblib


input_file = './datasets/symbolds/symb/GOOGL.csv'
with open(input_file, 'r') as f:
    reader = csv.reader(f)
    next(reader) 
    input_values = [list(map(float, row)) for row in reader]

input_df = pd.DataFrame(input_values, columns=['Open', 'High', 'Low', 'Volume'])

ridge_from_joblib = joblib.load('/StockPricePrediction-main/model.pkl')

predicted_prices = ridge_from_joblib.predict(input_df)

input_df['Predicted Price'] = predicted_prices

# save predicted prices to CSV 
output_file = './datasets/symbolds/op/OP_GOOGL.csv'
input_df.to_csv(output_file, index=False)

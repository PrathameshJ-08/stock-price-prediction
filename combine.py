# To combine Closing price actual and predicted csv files


import pandas as pd

# Closing closing prices and dates
Closing_df = pd.read_csv('/datasets/symbolds/symb/TSLA.csv')
Closing_df = Closing_df[['Date', 'Close']]

# predicted closing prices
Predicted_Closing = pd.read_csv('datasets/symbolds/symb/op/OP_TSLA.csv')
Predicted_Closing = Predicted_Closing[['Predicted Price']]

combined_df = pd.concat([Closing_df, Predicted_Closing], axis=1)

# new combined CSV 
combined_df.to_csv('./datasets/symbolds/symb/combine/C_TSLA.csv', index=False)

from flask import Flask, render_template, request
import utils
import plotly.graph_objs as go
import pandas as pd
import os
import time

import yfinance as yf

def calculate_adv_decl_ratio(symbol):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")
    advances = data[data['Close'] > data['Open']].count()['Close']
    declines = data[data['Close'] < data['Open']].count()['Close']
    ratio = advances / declines
    return ratio


app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/predict/', methods = ['GET', 'POST'])
def predict():
    if request.method == 'POST':
        Open = request.form.get('Open')
        High = request.form.get('High')
        Low = request.form.get('Low')
        Volume = request.form.get('Volume')

    #prediction
    prediction = utils.preprocess(Open, High, Low, Volume)

    # Load the data 
    df = pd.read_csv('datasets/combined_data.csv')

    # scatter plot -actual close prices
    actual_plot = go.Scatter(
    x=df['Date'],
    y=df['Close'],
    mode='markers',
    name='Actual Close'
            
)

#  scatter plot - predicted close prices
    predicted_plot = go.Scatter(
    x=df['Date'],
    y=df['Predicted Price'],
    mode='markers',
    name='Predicted Price Close',
    
)

    # Create the layout for both plots
    layout = go.Layout(
    title=dict(
        text='Actual VS Predicted Closing Prices',
        x=0.5,  # Set the title x-position to the center of the plot
        y=0.95  # Set the title y-position to the top of the plot
    ),

    xaxis={'title': 'Date', 'gridcolor': 'black'} ,
    yaxis={'title': 'Close Price', 'gridcolor': 'black'},
    plot_bgcolor='#293038', 
    paper_bgcolor='#293038',  
    font=dict(color='white')

)
    fig = go.Figure(data=[actual_plot, predicted_plot], layout=layout)
    plot_html = fig.to_html(full_html=False)
    symbols = symbols = {'AAPL': 'blue', 'AMZN': 'red', 'GOOGL': 'green', 'TSLA': 'orange', 'MSFT': 'purple'}
    traces = []
    for symbol, color in symbols.items():
        filename = 'C_'+symbol + '.csv'
        filepath = os.path.join('datasets/symbolds/symb/combine', filename)
        df = pd.read_csv(filepath)

        actual_plot = go.Scatter(
        x=df['Date'],
        y=df['Close'],
        mode='markers',
        name=symbol + 'Actual Close',
        marker=dict(color=color)
        )

        predicted_plot = go.Scatter(
        x=df['Date'],
        y=df['Predicted Price'],
        mode='markers',
        name=symbol + ' Predicted Close',
        marker=dict(color=color, symbol='triangle-up')
        )

        traces.append(actual_plot)
        traces.append(predicted_plot)

    layout = go.Layout(
    title='Stock Data',
    xaxis={'title': 'Date'},
    yaxis={'title': 'Close Price'}
    
)

    fig2 = go.Figure(data=traces, layout=layout)
    plot_html2 = fig2.to_html(full_html=False)
    return render_template('prediction.html', prediction=prediction, plot_html=plot_html, plot_html2=plot_html2)
time.sleep(5)


if __name__ == "__main__":
    app.run(debug=True)
    
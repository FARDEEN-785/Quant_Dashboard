from flask import Flask, render_template, request
from utils import get_crypto_data, get_coingecko_data, plot_technical_indicators
from strategy import apply_macd_strategy, enhanced_trading_strategy, calculate_sma, calculate_rsi

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    signal = None
    enhanced_signal = None
    data = None
    plot_url = None
    rsi_value = None
    sma_value = None

    if request.method == 'POST':
        symbol = request.form['symbol'].upper() + 'USDT'
        try:
            df = get_crypto_data(symbol)
            
            # Calculate all indicators
            df['SMA_20'] = calculate_sma(df, 20)
            df['RSI_14'] = calculate_rsi(df, 14)
            
            # Get signals from both strategies
            signal = apply_macd_strategy(df)
            enhanced_signal = enhanced_trading_strategy(df)
            
            # Get current indicator values
            rsi_value = round(df['RSI_14'].iloc[-1], 2)
            sma_value = round(df['SMA_20'].iloc[-1], 2)
            
            data = df.tail(5).to_html(classes='crypto-table')
            plot_url = plot_technical_indicators(df)
        except Exception as e:
            signal = f"Error fetching data: {e}"
            enhanced_signal = f"Error: {e}"

    return render_template('index.html', 
                         signal=signal, 
                         enhanced_signal=enhanced_signal,
                         data=data, 
                         plot_url=plot_url,
                         rsi_value=rsi_value,
                         sma_value=sma_value)

if __name__ == '__main__':
    app.run(debug=True)

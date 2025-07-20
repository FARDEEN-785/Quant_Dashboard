from flask import Flask, render_template, request
from utils import get_crypto_data, plot_macd
from strategy import apply_macd_strategy

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    signal = None
    data = None
    plot_url = None

    if request.method == 'POST':
        symbol = request.form['symbol'].upper() + 'USDT'
        try:
            df = get_crypto_data(symbol)
            signal = apply_macd_strategy(df)
            data = df.tail(5).to_html(classes='crypto-table')
            plot_url = plot_macd(df)
        except Exception as e:
            signal = f"Error fetching data: {e}"

    return render_template('index.html', signal=signal, data=data, plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)

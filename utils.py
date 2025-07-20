import pandas as pd
import requests
import matplotlib.pyplot as plt
import io
import base64

def get_crypto_data(symbol='BTCUSDT', interval='1d', limit=100):
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'
    response = requests.get(url)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        'timestamp', 'open', 'high', 'low', 'close',
        'volume', 'close_time', 'quote_asset_volume',
        'num_trades', 'taker_buy_base', 'taker_buy_quote', 'ignore'
    ])

    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['close'] = df['close'].astype(float)
    df.set_index('timestamp', inplace=True)

    return df

def plot_macd(df):
    df['EMA12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['EMA26'] = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = df['EMA12'] - df['EMA26']
    df['signal_line'] = df['macd'].ewm(span=9, adjust=False).mean()

    plt.figure(figsize=(10, 5))
    plt.plot(df.index, df['macd'], label='MACD', color='blue')
    plt.plot(df.index, df['signal_line'], label='Signal Line', color='red')
    plt.legend()
    plt.title('MACD Chart')
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return plot_url

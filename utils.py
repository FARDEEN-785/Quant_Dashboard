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

def get_coingecko_data(coin_id='bitcoin', days=30):
    """Alternative data source from CoinGecko API"""
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart'
    params = {'vs_currency': 'usd', 'days': days}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Convert CoinGecko data to similar format as Binance
        prices = data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'close'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        return df
    except Exception as e:
        print(f"CoinGecko API error: {e}")
        return None

def plot_technical_indicators(df):
    """Enhanced plot with all technical indicators"""
    from strategy import calculate_sma, calculate_rsi
    
    # Calculate indicators
    df['EMA12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['EMA26'] = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = df['EMA12'] - df['EMA26']
    df['signal_line'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['SMA_20'] = calculate_sma(df, 20)
    df['RSI_14'] = calculate_rsi(df, 14)
    
    # Create subplots
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10))
    
    # Price and Moving Averages
    ax1.plot(df.index, df['close'], label='Close Price', color='black', linewidth=1)
    ax1.plot(df.index, df['EMA12'], label='EMA 12', color='blue', linewidth=1)
    ax1.plot(df.index, df['EMA26'], label='EMA 26', color='red', linewidth=1)
    ax1.plot(df.index, df['SMA_20'], label='SMA 20', color='green', linewidth=1)
    ax1.set_title('Price & Moving Averages')
    ax1.legend()
    ax1.grid(True)
    
    # MACD
    ax2.plot(df.index, df['macd'], label='MACD', color='blue', linewidth=1)
    ax2.plot(df.index, df['signal_line'], label='Signal Line', color='red', linewidth=1)
    ax2.fill_between(df.index, df['macd'], df['signal_line'], where=df['macd'] > df['signal_line'], 
                    alpha=0.3, color='green', label='Bullish')
    ax2.fill_between(df.index, df['macd'], df['signal_line'], where=df['macd'] <= df['signal_line'], 
                    alpha=0.3, color='red', label='Bearish')
    ax2.set_title('MACD')
    ax2.legend()
    ax2.grid(True)
    
    # RSI
    ax3.plot(df.index, df['RSI_14'], label='RSI (14)', color='purple', linewidth=1)
    ax3.axhline(y=70, color='r', linestyle='--', alpha=0.7, label='Overbought (70)')
    ax3.axhline(y=30, color='g', linestyle='--', alpha=0.7, label='Oversold (30)')
    ax3.axhline(y=50, color='gray', linestyle='--', alpha=0.5)
    ax3.set_title('RSI')
    ax3.legend()
    ax3.grid(True)
    ax3.set_ylim(0, 100)
    
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return plot_url

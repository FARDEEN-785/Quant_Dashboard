def apply_macd_strategy(df):
    df['EMA12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['EMA26'] = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = df['EMA12'] - df['EMA26']
    df['signal_line'] = df['macd'].ewm(span=9, adjust=False).mean()

    if df['macd'].iloc[-1] > df['signal_line'].iloc[-1]:
        return "BUY"
    elif df['macd'].iloc[-1] < df['signal_line'].iloc[-1]:
        return "SELL"
    else:
        return "HOLD"

def calculate_sma(df, window=20):
    return df['close'].rolling(window=window).mean()

def calculate_rsi(df, window=14):
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def enhanced_trading_strategy(df):
    # Calculate all indicators
    df['SMA_20'] = calculate_sma(df, 20)
    df['SMA_50'] = calculate_sma(df, 50)
    df['RSI_14'] = calculate_rsi(df, 14)
    
    # MACD (already calculated in apply_macd_strategy)
    df['EMA12'] = df['close'].ewm(span=12, adjust=False).mean()
    df['EMA26'] = df['close'].ewm(span=26, adjust=False).mean()
    df['macd'] = df['EMA12'] - df['EMA26']
    df['signal_line'] = df['macd'].ewm(span=9, adjust=False).mean()
    
    # Multi-factor decision making
    buy_signals = 0
    sell_signals = 0
    
    # MACD Signal
    if df['macd'].iloc[-1] > df['signal_line'].iloc[-1]:
        buy_signals += 1
    else:
        sell_signals += 1
    
    # RSI Signal
    if df['RSI_14'].iloc[-1] < 30:  # Oversold
        buy_signals += 1
    elif df['RSI_14'].iloc[-1] > 70:  # Overbought
        sell_signals += 1
    
    # SMA Signal (Golden Cross/Death Cross)
    if df['SMA_20'].iloc[-1] > df['SMA_50'].iloc[-1]:
        buy_signals += 1
    else:
        sell_signals += 1
    
    # Final decision
    if buy_signals >= 2:
        return "STRONG BUY"
    elif buy_signals > sell_signals:
        return "BUY"
    elif sell_signals >= 2:
        return "STRONG SELL"
    elif sell_signals > buy_signals:
        return "SELL"
    else:
        return "HOLD"

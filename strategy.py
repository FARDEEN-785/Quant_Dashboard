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

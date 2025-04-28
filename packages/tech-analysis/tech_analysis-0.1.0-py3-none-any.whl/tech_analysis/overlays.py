from core import sma, ema

def moving_average_overlay(prices, periods=[20, 50, 200]):
    return {p: sma(prices, p) for p in periods}

def exponential_moving_average_overlay(prices, periods=[20, 50, 200]):
    return {p: ema(prices, p) for p in periods}

def donchian_channel(highs, lows, period=20):
    upper = [None if i < period else max(highs[i-period:i]) for i in range(len(highs))]
    lower = [None if i < period else min(lows[i-period:i]) for i in range(len(lows))]
    return upper, lower

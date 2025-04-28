from core import sma, ema

def rsi(prices, period=14):
    gains = [0]
    losses = [0]
    for i in range(1, len(prices)):
        change = prices[i] - prices[i-1]
        gains.append(max(change, 0))
        losses.append(abs(min(change, 0)))
    
    avg_gain = sma(gains, period)
    avg_loss = sma(losses, period)
    rs_index = [(avg_gain[i] / avg_loss[i]) if avg_loss[i] != 0 else 0 for i in range(len(avg_loss))]
    return [100 - (100 / (1 + rs)) if i >= period else None for i, rs in enumerate(rs_index)]

def macd(prices, fast=12, slow=26, signal=9):
    macd_line = [a - b for a, b in zip(ema(prices, fast), ema(prices, slow))]
    signal_line = ema(macd_line, signal)
    histogram = [m - s for m, s in zip(macd_line, signal_line)]
    return macd_line, signal_line, histogram

def bollinger_bands(prices, period=20, multiplier=2):
    sma_vals = sma(prices, period)
    upper, lower = [], []
    for i in range(len(prices)):
        if i < period:
            upper.append(None)
            lower.append(None)
        else:
            std_dev = (sum((x - sma_vals[i]) ** 2 for x in prices[i-period:i]) / period) ** 0.5
            upper.append(sma_vals[i] + multiplier * std_dev)
            lower.append(sma_vals[i] - multiplier * std_dev)
    return upper, lower

def stochastic_oscillator(highs, lows, closes, k_period=14, d_period=3):
    k_values = []
    for i in range(len(closes)):
        if i < k_period:
            k_values.append(None)
        else:
            lowest_low = min(lows[i - k_period:i])
            highest_high = max(highs[i - k_period:i])
            k = 100 * (closes[i] - lowest_low) / (highest_high - lowest_low) if highest_high != lowest_low else 0
            k_values.append(k)
    d_values = [None if i < d_period or k_values[i] is None else sum(k_values[i-d_period+1:i+1]) / d_period for i in range(len(k_values))]
    return k_values, d_values

def williams_r(highs, lows, closes, period=14):
    r_values = []
    for i in range(len(closes)):
        if i < period:
            r_values.append(None)
        else:
            highest_high = max(highs[i - period:i])
            lowest_low = min(lows[i - period:i])
            r = -100 * (highest_high - closes[i]) / (highest_high - lowest_low) if highest_high != lowest_low else 0
            r_values.append(r)
    return r_values

def atr(highs, lows, closes, period=14):
    tr = []
    for i in range(len(closes)):
        if i == 0:
            tr.append(highs[i] - lows[i])
        else:
            tr_val = max(highs[i] - lows[i], abs(highs[i] - closes[i-1]), abs(lows[i] - closes[i-1]))
            tr.append(tr_val)
    return sma(tr, period)


def roc(prices, period=12):
    return [((prices[i] - prices[i - period]) / prices[i - period]) * 100 if i >= period else None for i in range(len(prices))]

def trix(prices, period=15):
    single_ema = ema(prices, period)
    double_ema = ema(single_ema, period)
    triple_ema = ema(double_ema, period)
    return [((triple_ema[i] - triple_ema[i-1]) / triple_ema[i-1]) * 100 if i > 0 else None for i in range(len(triple_ema))]

def cci(highs, lows, closes, period=20):
    typical_price = [(h + l + c) / 3 for h, l, c in zip(highs, lows, closes)]
    tp_sma = sma(typical_price, period)
    cci_vals = []
    for i in range(len(typical_price)):
        if i < period:
            cci_vals.append(None)
        else:
            mean_dev = sum(abs(typical_price[j] - tp_sma[i]) for j in range(i - period + 1, i + 1)) / period
            cci = (typical_price[i] - tp_sma[i]) / (0.015 * mean_dev) if mean_dev != 0 else 0
            cci_vals.append(cci)
    return cci_vals


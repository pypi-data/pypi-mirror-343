def sma(data, period):
    return [sum(data[i - period:i]) / period if i >= period else None for i in range(len(data))]

def ema(data, period):
    ema_vals = []
    k = 2 / (period + 1)
    for i, price in enumerate(data):
        if i == 0:
            ema_vals.append(price)
        else:
            ema_vals.append(price * k + ema_vals[-1] * (1 - k))
    return ema_vals

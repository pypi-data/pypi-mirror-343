def obv(prices, volume):
    obv_vals = [0]
    for i in range(1, len(prices)):
        if prices[i] > prices[i-1]:
            obv_vals.append(obv_vals[-1] + volume[i])
        elif prices[i] < prices[i-1]:
            obv_vals.append(obv_vals[-1] - volume[i])
        else:
            obv_vals.append(obv_vals[-1])
    return obv_vals

def pvt(prices, volume):
    pvt_vals = [0]
    for i in range(1, len(prices)):
        change = (prices[i] - prices[i-1]) / prices[i-1]
        pvt_vals.append(pvt_vals[-1] + change * volume[i])
    return pvt_vals


def mfi(highs, lows, closes, volume, period=14):
    typical_prices = [(h + l + c) / 3 for h, l, c in zip(highs, lows, closes)]
    money_flows = [tp * v for tp, v in zip(typical_prices, volume)]
    pos_flow, neg_flow = [], []

    for i in range(1, len(typical_prices)):
        if typical_prices[i] > typical_prices[i-1]:
            pos_flow.append(money_flows[i])
            neg_flow.append(0)
        elif typical_prices[i] < typical_prices[i-1]:
            pos_flow.append(0)
            neg_flow.append(money_flows[i])
        else:
            pos_flow.append(0)
            neg_flow.append(0)

    mfi_vals = []
    for i in range(len(typical_prices)):
        if i < period:
            mfi_vals.append(None)
        else:
            pos_sum = sum(pos_flow[i - period + 1:i + 1])
            neg_sum = sum(neg_flow[i - period + 1:i + 1])
            mfr = pos_sum / neg_sum if neg_sum != 0 else 0
            mfi = 100 - (100 / (1 + mfr))
            mfi_vals.append(mfi)
    return mfi_vals


def chaikin_money_flow(highs, lows, closes, volumes, period=20):
    mfv = []
    for h, l, c, v in zip(highs, lows, closes, volumes):
        if h != l:
            mf_multiplier = ((c - l) - (h - c)) / (h - l)
        else:
            mf_multiplier = 0
        mfv.append(mf_multiplier * v)

    return [None if i < period else sum(mfv[i-period+1:i+1]) / sum(volumes[i-period+1:i+1]) for i in range(len(closes))]

def ease_of_movement(highs, lows, volumes, period=14):
    emv = []
    for i in range(1, len(highs)):
        distance = ((highs[i] + lows[i]) / 2) - ((highs[i-1] + lows[i-1]) / 2)
        box_ratio = volumes[i] / (highs[i] - lows[i]) if (highs[i] - lows[i]) != 0 else 0
        emv.append(distance / box_ratio if box_ratio != 0 else 0)
    return [None if i < period else sum(emv[i - period + 1:i + 1]) / period for i in range(len(emv))]

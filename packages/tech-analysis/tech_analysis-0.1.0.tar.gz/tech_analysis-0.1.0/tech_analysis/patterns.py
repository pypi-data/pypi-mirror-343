def is_doji(open_, close, threshold=0.1):
    return [abs(o - c) <= threshold * max(o, c) for o, c in zip(open_, close)]

def is_hammer(open_, high, low, close):
    result = []
    for o, h, l, c in zip(open_, high, low, close):
        body = abs(c - o)
        lower_shadow = min(o, c) - l
        upper_shadow = h - max(o, c)
        result.append(lower_shadow > 2 * body and upper_shadow < body)
    return result

def is_inverted_hammer(open_, high, low, close):
    result = []
    for o, h, l, c in zip(open_, high, low, close):
        body = abs(c - o)
        upper_shadow = h - max(o, c)
        lower_shadow = min(o, c) - l
        result.append(upper_shadow > 2 * body and lower_shadow < body)
    return result

def is_shooting_star(open_, high, low, close):
    return is_inverted_hammer(open_, high, low, close)  # Same shape, different context

def is_bullish_engulfing(open_, close):
    return [
        i > 0 and close[i-1] < open_[i-1] and close[i] > open_[i] and close[i] > open_[i-1] and open_[i] < close[i-1]
        for i in range(len(close))
    ]

def is_bearish_engulfing(open_, close):
    return [
        i > 0 and close[i-1] > open_[i-1] and close[i] < open_[i] and open_[i] > close[i-1] and close[i] < open_[i-1]
        for i in range(len(close))
    ]

def is_bullish_harami(open_, close):
    return [
        i > 0 and close[i-1] < open_[i-1] and close[i] > open_[i] and close[i] < open_[i-1] and open_[i] > close[i-1]
        for i in range(len(close))
    ]

def is_bearish_harami(open_, close):
    return [
        i > 0 and close[i-1] > open_[i-1] and close[i] < open_[i] and close[i] > open_[i-1] and open_[i] < close[i-1]
        for i in range(len(close))
    ]

def is_morning_star(open_, close):
    return [
        i > 1 and close[i-2] < open_[i-2] and abs(close[i-1] - open_[i-1]) < 0.2 * abs(open_[i-2] - close[i-2]) and close[i] > open_[i]
        and close[i] > ((open_[i-2] + close[i-2]) / 2)
        for i in range(len(close))
    ]

def is_evening_star(open_, close):
    return [
        i > 1 and close[i-2] > open_[i-2] and abs(close[i-1] - open_[i-1]) < 0.2 * abs(open_[i-2] - close[i-2]) and close[i] < open_[i]
        and close[i] < ((open_[i-2] + close[i-2]) / 2)
        for i in range(len(close))
    ]

def is_three_white_soldiers(open_, close):
    result = []
    for i in range(2, len(close)):
        result.append(
            close[i-2] < open_[i-2] and
            close[i-1] > open_[i-1] and close[i-1] > close[i-2] and
            close[i] > open_[i] and close[i] > close[i-1]
        )
    return result

def is_three_black_crows(open_, close):
    result = []
    for i in range(2, len(close)):
        result.append(
            close[i-2] > open_[i-2] and
            close[i-1] < open_[i-1] and close[i-1] < close[i-2] and
            close[i] < open_[i] and close[i] < close[i-1]
        )
    return result

def is_tweezer_top(open_, close):
    return [i > 0 and abs(close[i] - close[i-1]) < 0.1 and close[i] < open_[i] and close[i-1] < open_[i-1] for i in range(len(close))]

def is_tweezer_bottom(open_, close):
    return [i > 0 and abs(close[i] - close[i-1]) < 0.1 and close[i] > open_[i] and close[i-1] > open_[i-1] for i in range(len(close))]

def is_piercing_line(open_, close):
    return [
        i > 0 and close[i-1] < open_[i-1] and close[i] > open_[i] and
        open_[i] < close[i-1] and close[i] > (open_[i-1] + close[i-1]) / 2
        for i in range(len(close))
    ]

def is_dark_cloud_cover(open_, close):
    return [
        i > 0 and close[i-1] > open_[i-1] and close[i] < open_[i] and
        open_[i] > close[i-1] and close[i] < (open_[i-1] + close[i-1]) / 2
        for i in range(len(close))
    ]

def is_rising_three_methods(open_, close):
    return [
        i > 3 and close[i-4] < open_[i-4] and
        all(close[j] < open_[j] for j in range(i-3, i)) and
        close[i] > open_[i] and close[i] > close[i-4]
        for i in range(len(close))
    ]

def is_falling_three_methods(open_, close):
    return [
        i > 3 and close[i-4] > open_[i-4] and
        all(close[j] > open_[j] for j in range(i-3, i)) and
        close[i] < open_[i] and close[i] < close[i-4]
        for i in range(len(close))
    ]

def is_inside_bar(high, low):
    return [
        i > 0 and high[i] < high[i-1] and low[i] > low[i-1]
        for i in range(len(high))
    ]

def is_outside_bar(high, low):
    return [
        i > 0 and high[i] > high[i-1] and low[i] < low[i-1]
        for i in range(len(high))
    ]

def is_marubozu(open_, close, threshold=0.01):
    return [
        abs(o - c) / max(o, c) > (1 - threshold) for o, c in zip(open_, close)
    ]

def is_inside_day_breakout(high, low):
    inside = is_inside_bar(high, low)
    breakout = []
    for i in range(2, len(high)):
        if inside[i-1]:
            breakout.append(high[i] > high[i-2] or low[i] < low[i-2])
        else:
            breakout.append(False)
    return [False, False] + breakout

def break_of_structure(high, low):
    bos = []
    for i in range(1, len(high)):
        if high[i] > max(high[:i]):
            bos.append("bullish")
        elif low[i] < min(low[:i]):
            bos.append("bearish")
        else:
            bos.append(None)
    return bos


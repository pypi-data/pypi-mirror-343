# tech_analysis/breadth.py

def advance_decline(advancing, declining):
    ad_line = [0]
    for a, d in zip(advancing, declining):
        ad_line.append(ad_line[-1] + (a - d))
    return ad_line[1:]

def advance_decline_ratio(advancing, declining):
    return [(a / d) if d != 0 else 0 for a, d in zip(advancing, declining)]

def new_highs_lows(new_highs, new_lows):
    return [h - l for h, l in zip(new_highs, new_lows)]

def trinar_indicator(advancing, declining, unchanged):
    return [(a - d) / (a + d + u) if (a + d + u) != 0 else 0 for a, d, u in zip(advancing, declining, unchanged)]

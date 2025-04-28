def position_size(account_size, risk_per_trade, stop_loss_pips, pip_value):
    risk_amount = account_size * risk_per_trade
    return int(risk_amount / (stop_loss_pips * pip_value))

def max_drawdown(values):
    peak = values[0]
    max_dd = 0
    for v in values:
        if v > peak:
            peak = v
        dd = (peak - v) / peak
        if dd > max_dd:
            max_dd = dd
    return max_dd

def value_at_risk(returns, confidence=0.95):
    sorted_returns = sorted(returns)
    index = int((1 - confidence) * len(sorted_returns))
    return -sorted_returns[index]

def kelly_criterion(win_prob, win_loss_ratio):
    return win_prob - (1 - win_prob) / win_loss_ratio

def risk_of_ruin(win_rate, loss_rate, avg_win, avg_loss):
    edge = (win_rate * avg_win) - (loss_rate * avg_loss)
    variance = (win_rate * avg_win ** 2) + (loss_rate * avg_loss ** 2)
    return edge / (variance ** 0.5) if variance != 0 else 0

def monte_carlo_simulation(initial_balance, trades, simulations=1000):
    from random import choice
    results = []
    for _ in range(simulations):
        balance = initial_balance
        for _ in range(len(trades)):
            balance += choice(trades)
        results.append(balance)
    return results

from tech_analysis.risk import max_drawdown

def sharpe_ratio(returns, risk_free=0.0):
    excess = [r - risk_free for r in returns]
    avg = sum(excess) / len(excess)
    std = (sum((x - avg) ** 2 for x in excess) / len(excess)) ** 0.5
    return avg / std if std != 0 else 0

def sortino_ratio(returns, risk_free=0.0):
    excess = [r - risk_free for r in returns]
    downside = [min(0, r) for r in excess]
    downside_dev = (sum(x**2 for x in downside) / len(downside)) ** 0.5
    avg = sum(excess) / len(excess)
    return avg / downside_dev if downside_dev != 0 else 0

def cagr(values, periods_per_year):
    start = values[0]
    end = values[-1]
    n = len(values) / periods_per_year
    return (end / start) ** (1 / n) - 1


def max_return(values):
    return max(values[i] - values[j] for i in range(len(values)) for j in range(i))

def volatility(returns):
    avg = sum(returns) / len(returns)
    return (sum((r - avg) ** 2 for r in returns) / len(returns)) ** 0.5

def calmar_ratio(returns, values):
    cagr_val = cagr(values, periods_per_year=252)
    mdd = max_drawdown(values)
    return cagr_val / mdd if mdd != 0 else 0

def beta(asset_returns, benchmark_returns):
    avg_asset = sum(asset_returns) / len(asset_returns)
    avg_benchmark = sum(benchmark_returns) / len(benchmark_returns)
    cov = sum((a - avg_asset) * (b - avg_benchmark) for a, b in zip(asset_returns, benchmark_returns))
    var = sum((b - avg_benchmark) ** 2 for b in benchmark_returns)
    return cov / var if var != 0 else 0

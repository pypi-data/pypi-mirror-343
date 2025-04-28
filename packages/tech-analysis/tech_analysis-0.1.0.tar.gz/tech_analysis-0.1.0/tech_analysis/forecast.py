def linear_regression(x, y):
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xx = sum([i**2 for i in x])
    sum_xy = sum([x[i] * y[i] for i in range(n)])
    b = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x**2)
    a = (sum_y - b * sum_x) / n
    return a, b

def predict_linear(x, a, b):
    return [a + b * xi for xi in x]

def moving_average(series, window=5):
    return [round(sum(series[i:i+window]) / window, 2)
            for i in range(len(series) - window)]

def mean_squared_error(y_true, y_pred):
    return sum([(y_true[i] - y_pred[i]) ** 2 for i in range(len(y_pred))]) / len(y_pred)


def visualize_ascii(actual, predicted, step=5):
    print("\nASCII Forecast Visualization:")
    for i in range(0, min(len(actual), len(predicted)), step):
        a = int(actual[i] // 5)
        p = int(predicted[i] // 5)
        print(f"{i:3d}: {'*' * a} | {'-' * p}")


def forecast_stock(data, method="linear", window=5):
    if not data or len(data) < window + 1:
        raise ValueError("Insufficient data provided.")

    x = list(range(len(data)))

    if method == "linear":
        a, b = linear_regression(x, data)
        prediction = predict_linear(x, a, b)
        trimmed_actual = data
    elif method == "moving_avg":
        prediction = moving_average(data, window)
        trimmed_actual = data[len(data) - len(prediction):]
    else:
        raise ValueError("Unsupported forecasting method")

    mse = mean_squared_error(trimmed_actual, prediction)
    return {
        "actual": trimmed_actual,
        "predicted": prediction,
        "mse": mse
    }


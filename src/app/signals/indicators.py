from typing import List


def simple_moving_average(values: List[float], window: int) -> float:
    if len(values) < window:
        raise ValueError("Not enough data for SMA")

    return sum(values[-window:]) / window


def relative_strength_index(values: List[float], window: int = 14) -> float:
    if len(values) < window + 1:
        raise ValueError("Not enough data for RSI")

    gains = []
    losses = []

    for i in range(-window, 0):
        delta = values[i] - values[i - 1]
        if delta >= 0:
            gains.append(delta)
        else:
            losses.append(abs(delta))

    average_gain = sum(gains) / window
    average_loss = sum(losses) / window if losses else 0.0001

    rs = average_gain / average_loss
    return 100 - (100 / (1 + rs))

import pandas as pd
import time
from collections import deque


def calculate_ema(new_value, prev_ema, window):
    """Efficiently calculates the Exponential Moving Average (EMA) for a new tick."""
    alpha = 2 / (window + 1)
    return new_value if prev_ema is None else alpha * new_value + (1 - alpha) * prev_ema


def find_different_value(data, x, last_value):
    """
    Searches the array from the end for a number that differs from
    the last number by at least x.

    Returns:
        The index of the found element in the array or 0 if no such element exists.
    """
    for i in range(len(data) - 4, -1, -1):  # Iterate from the end of the array
        if abs(data[i] - last_value) >= x:
            return i  # Return index
    return 0  # No such element found


def trade_logic(file_path, size_cash=20.5, window_size=10,
                window_size_long=50, size_swim_window=2):
    output_csv = "trade_results.csv"

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return
    except pd.errors.EmptyDataError:
        print(f"File {file_path} is empty.")
        return

    required_cols = ['best_bid', 'best_ask']
    if not all(col in df.columns for col in required_cols):
        print(f"CSV file must contain columns: {', '.join(required_cols)}.")
        return

    best_bid = df['best_bid'].values
    best_ask = df['best_ask'].values

    cash = best_ask[0] * size_cash  # Initial capital
    cash0 = cash
    bear_assets = 0
    bull_assets = 0
    last_price_purchase = 0
    last_last_price_purchase = 0
    average_btd = 0
    average_price_bag = 0
    data_records = []

    bid_history = deque(maxlen=window_size_long)  # Stores bid price history
    bid_smooth_history = deque(maxlen=window_size_long)  # Stores smoothed bids

    ema_swim_bid = None
    ema_bid = None
    value_bid_last = 0
    delta_ema = 0
    delta_ema_swim = 0
    sma_long_bid_last = 0
    ema_swim_bid_last = 0
    bid_std = None

    for j, (value_bid, value_ask) in enumerate(zip(best_bid, best_ask)):
        bid_history.append(value_bid)

        # Skip until enough data is accumulated
        if len(bid_history) < window_size:
            continue

        # Update EMA and standard deviation efficiently
        ema_bid = calculate_ema(value_bid, ema_bid, window_size)

        if bid_std is None:
            bid_std = pd.Series(bid_history).std()
        else:
            bid_std = (bid_std * (j - 1) + abs(value_bid - ema_bid)) / j

        average_btd = (average_btd * (j - 1) + bid_std) / j

        if abs(value_bid - ema_bid) > average_btd and \
                abs(value_bid_last - ema_bid) > average_btd:
            bid_smooth_history.append(value_bid)
        else:
            bid_smooth_history.append(ema_bid)

        # Skip until long-term window is filled
        if len(bid_history) < window_size_long:
            continue

        swim_window = window_size_long - 1 - find_different_value(
            list(bid_history), size_swim_window * average_btd, bid_history[-1]
        )

        ema_swim_bid = calculate_ema(bid_smooth_history[-1],
                                     ema_swim_bid, swim_window)

        # Calculate squared deviation of different moving averages
        delta_ema += (ema_bid - value_bid) ** 2
        delta_ema_swim += (ema_swim_bid - value_bid) ** 2

        # Simple Moving Average (SMA) without redundant Series creation
        sma_long_bid = sum(bid_history) / window_size_long

        # Trading logic
        # Condition to sell 1 asset
        if value_bid > last_price_purchase and bear_assets > 0:
            cash += bear_assets * value_bid
            bear_assets = 0

        # Condition to buy 1 asset
        elif cash > value_ask:
            if value_ask < ema_swim_bid and ema_swim_bid > sma_long_bid and ema_swim_bid > ema_swim_bid_last:
                bear_assets += 1
                cash -= value_ask
                if bear_assets > 1:
                    last_last_price_purchase = last_price_purchase
                last_price_purchase = value_ask

        # Condition for forced sale of half the assets
        elif int(cash / value_ask) == 0 and ema_swim_bid > ema_swim_bid_last \
                and ema_swim_bid < sma_long_bid and bull_assets > 1:
            sell_count = bull_assets // 2
            cash += sell_count * value_bid
            bull_assets -= sell_count

        # Condition for transferring an asset to long
        if bear_assets > 1:
            bull_assets += 1
            average_price_bag = (average_price_bag * (bull_assets - 1) +
                                 last_last_price_purchase) / bull_assets
            bear_assets = 1

        # Condition to sell long assets
        if value_bid > average_price_bag and ema_swim_bid > ema_swim_bid_last \
                and ema_swim_bid < sma_long_bid and bull_assets > 0:
            cash += bull_assets * value_bid
            bull_assets = 0
            average_price_bag = 0

        ema_swim_bid_last = ema_swim_bid
        sma_long_bid_last = sma_long_bid
        value_bid_last = value_bid

        total_profit = (cash + (bear_assets + bull_assets) * value_bid) / cash0
        data_records.append([
            j, value_bid, value_ask, bear_assets + bull_assets, cash,
            ema_swim_bid, total_profit
        ])

    df_results = pd.DataFrame(
        data_records,
        columns=['time_step', 'best_bid', 'best_ask', 'assets',
                 'ema_swim_bid', 'cash', 'total_profit']
    )
    df_results.to_csv(output_csv, index=False)

    print(f"Total Profit: {total_profit:.6f}")


if __name__ == "__main__":
    file_path = 'best_bid_ask_data8.csv'
    trade_logic(file_path)


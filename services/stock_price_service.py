import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def generate_stock_prices(T: int):
    dt = 1 / 30

    time_scale = T / 100

    stock_names = ["STOCK_A", "STOCK_B", "STOCK_C", "STOCK_D", "STOCK_E"]

    price_base = {
        "STOCK_A": np.random.uniform(0, 10000),
        "STOCK_B": np.random.uniform(10000, 20000),
        "STOCK_C": np.random.uniform(0, 2000),
        "STOCK_D": np.random.uniform(3000, 6000),
        "STOCK_E": np.random.uniform(2000, 7000)
    }

    price_multipliers = {
        "STOCK_A": price_base["STOCK_A"] / 1000,
        "STOCK_B": price_base["STOCK_B"] / 1000,
        "STOCK_C": price_base["STOCK_C"] / 1000,
        "STOCK_D": price_base["STOCK_D"] / 1000,
        "STOCK_E": price_base["STOCK_E"] / 1000
    }


    while True:
        assets = {
            name: {
                "mu": np.random.uniform(0.1, 0.15),
                "sigma": np.random.uniform(0.25, 0.30)
            }
            for name in stock_names
        }

        roles = np.random.permutation(stock_names)
        pump_stock     = roles[0]
        decoy_stock_1  = roles[1]
        mount_stock_1  = roles[2]
        mount_stock_2  = roles[3]
        crash_stock    = roles[4]

        prices = pd.DataFrame(index=range(T))

        for name, params in assets.items():
            mu_base = params["mu"]
            sigma_base = params["sigma"]

            Z = np.random.standard_normal(T)
            S = np.zeros(T)

            S[0] = np.random.uniform(50, 150)
            pump_start   = int(np.random.uniform(70, 90) * time_scale)
            decoy_start  = int(np.random.uniform(20, 40) * time_scale)
            decoy_end    = int(np.random.uniform(45, 60) * time_scale)
            decoy_middle = int((decoy_end - decoy_start) / 2 + decoy_start)

            crash_start  = int(np.random.uniform(40, 60) * time_scale)
            crash_middle = int(np.random.uniform(65, 80) * time_scale)

            mid_start = int(np.random.uniform(30, 40) * time_scale)
            mid_peak  = int(np.random.uniform(45, 55) * time_scale)
            mid_end   = int(np.random.uniform(60, 70) * time_scale)

            for t in range(1, T):
                mu = mu_base
                sigma = sigma_base
                shock = 0.0

                if name in [mount_stock_1, mount_stock_2]:
                    if mid_start <= t <= mid_peak:
                        mu += np.random.uniform(0.8, 1.2)
                        sigma *= 1.2
                    elif mid_peak < t <= mid_end:
                        mu -= np.random.uniform(0.8, 1.2)
                        sigma *= 0.8

                if name == decoy_stock_1 and t >= decoy_start:
                    if decoy_start <= t <= decoy_middle:
                        mu -= np.random.uniform(0.8, 1.2)
                        sigma *= 1.2
                    elif t <= decoy_end:
                        mu += np.random.uniform(0.8, 1.2)
                        sigma *= 0.8

                if name == pump_stock and t >= decoy_start:
                    if decoy_start <= t <= decoy_middle:
                        mu -= np.random.uniform(0.8, 1.2)
                        sigma *= 1.2
                    elif t <= decoy_end:
                        mu += np.random.uniform(0.8, 1.2)
                        sigma *= 0.8

                if name == pump_stock and t >= pump_start:
                    mu += np.random.uniform(0.5, 2.0)
                    sigma *= 1.4
                    if np.random.rand() < 0.15:
                        shock += np.random.uniform(0.1, 0.2)

                if name in [crash_stock, decoy_stock_1]:
                    if crash_start <= t <= crash_middle:
                        mu -= np.random.uniform(0.4, 1.5)
                        sigma *= 0.9
                    elif t > crash_middle:
                        mu -= np.random.uniform(0.5, 2.0)

                S[t] = S[t-1] * np.exp(
                    (mu - 0.5 * sigma**2) * dt
                    + sigma * np.sqrt(dt) * Z[t]
                    + shock
                )

            prices[name] = S

        if all((prices[col].max() - prices[col].min()) >= 125 for col in prices.columns):
            condition_met = False
            for col in prices.columns:
                if 1500 > prices[col].max() > 400 and prices[col].min() < prices[col].max() / 6:
                    condition_met = True
                    break
            if condition_met:
                break

    #可視化用に残しておく
    """
    # ===== 可視化 =====
    plt.figure(figsize=(12, 6))
    for col in prices.columns:
        plt.plot(prices[col], label=col)
    plt.xlabel("days")
    plt.ylabel("price")
    plt.legend()
    plt.grid(True)
    plt.show()
    
    """

    for name in stock_names:
        prices[name] = prices[name] * price_multipliers[name] + price_base[name]

    daily_prices: list[list[float]] = []

    for t in range(T):
        day_prices = [prices[name].iloc[t] for name in stock_names]
        daily_prices.append(day_prices)

    return daily_prices
import numpy as np
import matplotlib.pyplot as plt

class Trader:
    def __init__(self, strategy="random", size=1.0):
        self.strategy = strategy
        self.size = size
        self.last_price = None

    def act(self, mid_price, order_book, order_jitter=0.01):
        if self.strategy == "random":
            price = mid_price * (1 + order_jitter * np.random.randn())
            return price, "random"

        elif self.strategy == "trend":
            if self.last_price is None:
                self.last_price = mid_price
                return mid_price, "trend"
            delta = mid_price - self.last_price
            self.last_price = mid_price
            if delta > 0:
                price = mid_price * 1.01
            else:
                price = mid_price * 0.99
            return price, "trend"

        elif self.strategy == "hft":
            if np.random.rand() > 0.5:
                price = mid_price * 0.998
            else:
                price = mid_price * 1.002
            return price, "hft"

        elif self.strategy == "whale":
            price = mid_price * (1 + order_jitter * np.random.randn())
            return price, "whale"

def simulate_market(steps=500, n_traders=300, whale_ratio=0.05, trend_ratio=0.2, hft_ratio=0.2):
    order_book = []
    prices = []
    traders = []

    for _ in range(n_traders):
        r = np.random.rand()
        if r < whale_ratio:
            traders.append(Trader(strategy="whale", size=20.0))
        elif r < whale_ratio + trend_ratio:
            traders.append(Trader(strategy="trend"))
        elif r < whale_ratio + trend_ratio + hft_ratio:
            traders.append(Trader(strategy="hft"))
        else:
            traders.append(Trader(strategy="random"))

    order_book.append(100.0)

    for step in range(steps):
        mid_price = np.mean(order_book[-min(len(order_book), 50):])
        prices.append(mid_price)

        for trader in traders:
            price, strategy = trader.act(mid_price, order_book)
            if len(order_book) > 0:
                closest = min(order_book, key=lambda x: abs(x - price))
                order_book.remove(closest)
            order_book.append(price)

    return prices

def plot_prices(prices):
    plt.plot(prices)
    plt.title("Simulated Market Prices")
    plt.xlabel("Time")
    plt.ylabel("Price")
    plt.grid(True)
    plt.show()

prices = simulate_market()
plot_prices(prices)

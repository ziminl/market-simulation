import numpy as np
import matplotlib.pyplot as plt

class Order:
    def __init__(self, price, size=1):
        self.price, self.size = price, size

def run_sim(n_steps=10000, init_price=100.0, n_ticks=1000, order_jitter=0.01):
    order_book = []
    mid = init_price
    prices = [mid]
    for _ in range(n_ticks):
        p = mid * (1 + order_jitter * np.random.randn())
        order_book.append(Order(p))
    for _ in range(n_steps):
        mid_price = prices[-1]
        p = mid_price * (1 + order_jitter * np.random.randn())
        diffs = [abs(o.price - p) for o in order_book]
        idx = np.argmin(diffs)
        mid = order_book[idx].price
        prices.append(mid)
        new_p = mid * (1 + order_jitter * np.random.randn())
        order_book[idx] = Order(new_p)
    return prices

if __name__ == "__main__":
    prices = run_sim()
    plt.plot(prices)
    plt.title("Random-Trader Simulation Price Evolution")
    plt.xlabel("Time step")
    plt.ylabel("Price")
    plt.show()

import numpy as np

class Intristic_Growth:
    def __init__(self, FCFF0, wacc, years=5, g_min=-0.2, g_max=0.2, n=2001):
        self.FCFF0 = float(FCFF0)
        self.wacc = float(wacc)
        self.years = int(years)
        self.g_min = float(g_min)
        self.g_max = float(g_max)
        self.n = int(n)

    def EV(self, g, years=None):
        years = self.years if years is None else int(years)
        g = float(g)

        fcff = self.FCFF0
        pv_sum = 0.0

        for t in range(1, years + 1):
            fcff *= (1.0 + g)
            pv_sum += fcff / ((1.0 + self.wacc) ** t)

        terminal_value = fcff / self.wacc 
        pv_terminal = terminal_value / ((1.0 + self.wacc) ** years)

        return pv_sum + pv_terminal

    def solve_implied_growth(self, market_equity_value, years=None):
        years = self.years if years is None else int(years)
        market_equity_value = float(market_equity_value)

        growths = np.linspace(self.g_min, self.g_max, self.n)
        values = np.array([self.EV(g, years) for g in growths])

        idx = int(np.argmin(np.abs(values - market_equity_value)))
        implied_g = float(growths[idx])
        implied_value = float(values[idx])

        return implied_g, implied_value

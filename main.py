import pandas as pd
from fundmentals import Fundmentals
import yfinance as yf
from datetime import date
from intristic_growth import Intristic_Growth

### --- Getting Financial Data ---
### Used for calculating the Intrinsic Value

TICKER = "AAPL"
INVESTED_CAP_2025 = 191.2e9
NOPAT_2025 = 93.7e9
IMPLIED_GROWTH_2025 = -0.035
RATING = "AAA"

ticker = yf.Ticker(TICKER)

income       = ticker.income_stmt
balance_sheet = ticker.balance_sheet
cash_flow     = ticker.cashflow

init = Fundmentals(income, balance_sheet, cash_flow)
init.getIncomeData()
init.getBalanceData(INVESTED_CAP_2025)
init.getCashData()
init.createData(NOPAT_2025, IMPLIED_GROWTH_2025)
init.createWACC(ticker.info.get("beta"), RATING, ticker.info.get("marketCap"))

FCFF, ROIC, ROIIC, implied_growth, wacc = init.returnData()
netDebt = init.getNetDebt()
shares  = ticker.info.get("sharesOutstanding")
price   = yf.download(TICKER,start=date.today())["Close"][TICKER][0]

market_val = price * shares
FCFF0 = float(FCFF.sort_index().iloc[-1])
g0 = float(implied_growth.sort_index().iloc[-1])
wacc0 = float(wacc.sort_index().iloc[-1])

intr = Intristic_Growth(FCFF0, wacc0, years=5)

EV_intrinsic = intr.EV(g0)

equity_value = EV_intrinsic - netDebt
intrinsic_shareP = equity_value / shares

g_market, value_matched = intr.solve_implied_growth(market_val)

print("\n")

df_check = pd.DataFrame({
    "ROIC" : ROIC,
    "ROIIC" : ROIIC,
    "Growth" : implied_growth,
    "WACC" : wacc
})

print(df_check)
print(f"\nImplied Growth : {g_market}")
print(f"\nIntrinsic Stock Val: {intrinsic_shareP[0]}")
print(f"Current Price : {price}")

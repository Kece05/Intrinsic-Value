import pandas as pd
import yfinance as yf
import warnings
warnings.filterwarnings("ignore")

class Fundmentals:

    def __init__(self, income, balance, cash):
        self.income  = income
        self.balance = balance
        self.cashflow    = cash
    
    def getIncomeData(self):
        self.EBIT   = self.income.loc["EBIT"]
        self.preTax = self.income.loc["Pretax Income"]
        self.tax    = self.income.loc["Tax Provision"]

    def getBalanceData(self, implied_invest):
        self.cash        = self.balance.loc["Cash And Cash Equivalents"]
        self.totalDebt   = self.balance.loc["Total Debt"]
        self.investedCap = self.balance.loc["Invested Capital"]
        self.investedCap["2021-09-30"] = implied_invest
    
    def getNetDebt(self):
        return self.totalDebt - self.cash

    def getCashData(self):
        self.capEx      = -self.cashflow.loc["Capital Expenditure"]
        self.cap_Change = self.cashflow.loc["Change In Working Capital"]
        self.DA         = self.cashflow.loc["Depreciation And Amortization"]

    def createData(self, NOPAT_final, implied_growth_final):
        self.taxRate = (self.tax/self.preTax).clip(0,1)
        self.NOPAT = self.EBIT * (1 - self.taxRate)
        self.NOPAT["2021-09-30"] = NOPAT_final
        self.ROIC = self.NOPAT / self.investedCap

        self.dNOPAT = self.NOPAT.diff(periods=-1)
        self.dIC    = self.investedCap.diff(periods=-1)
        self.ROIIC  = self.dNOPAT / self.dIC

        self.FCFF = (self.NOPAT + self.DA - self.capEx - self.cap_Change)

        self.reinvestment_rate            = self.dIC / self.NOPAT.shift(1)
        self.implied_growth               = self.reinvestment_rate * self.ROIIC
        self.implied_growth["2025-09-30"] = implied_growth_final

    def cost_of_debt_from_rating(self, rating):
        spreads = {
            "AAA": 0.005,
            "AA":  0.006,
            "A":   0.010,
            "BBB": 0.015,
            "BB": 0.02,
            "B": 0.025
        }
        self.CoD = self.rf + spreads.get(rating, 0.012)

    def calculate_CAPM(self, beta):
        self.market_df = yf.download("^GSPC", start="1960-01-01", progress=False)
        self.tnx_df    = yf.download("^TNX",  start="1960-01-01", progress=False)

        self.market = self.market_df["Adj Close"] if "Adj Close" in self.market_df.columns else self.market_df["Close"]
        self.tnx    = (self.tnx_df["Adj Close"] if "Adj Close" in self.tnx_df.columns else self.tnx_df["Close"]) / 100

        market_ret = self.market.resample("Y").last().pct_change()
        rf_year    = self.tnx.resample("Y").mean()

        self.df = pd.concat([market_ret, rf_year], axis=1)
        self.df.columns = ["Rm", "Rf"]
        self.df = self.df.dropna()

        self.erp = float((self.df["Rm"] - self.df["Rf"]).mean())
        self.rf  = float(self.tnx.dropna().iloc[-1])

        self.CAPM = self.rf + beta * self.erp

    def createWACC(self, beta, rating, makertCap):
        self.calculate_CAPM(beta)
        self.cost_of_debt_from_rating(rating)

        self.V = self.totalDebt + makertCap

        self.wacc = (makertCap/self.V)*self.CAPM + (self.totalDebt / self.V)*(self.CoD * (1 - self.taxRate))

    def returnData(self):
        return self.FCFF, self.ROIC, self.ROIIC, self.implied_growth, self.wacc

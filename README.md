# Intrinsic Value & Market-Implied Growth Framework

## Overview
This project was inspired by reading *Pitch the Perfect Investment*, which emphasizes understanding what expectations are embedded in a stock’s price, rather than relying solely on forecasts or narratives.

While reading the book, I wanted to apply these ideas quantitatively. That led to building a framework that decomposes valuation into fundamental growth, market-implied growth, and intrinsic value, all derived from financial statements and first-principles relationships.

Core question this project answers:
Is the current stock price justified by the growth the business is actually capable of delivering?

---

## Core Idea
Markets don’t reward growth, they reward growth above expectations.

This framework separates valuation into three distinct components:

- Reinvestment-Implied Growth
- Market-Implied Growth
- Intrinsic Value per Share

By comparing these components, the model highlights expectation gaps, which are often the true drivers of long-term investment returns.

---

## Methodology

### 1. Derived Fundamental Metrics
All core financial metrics are derived directly from financial statements, including:

- ROIC (Return on Invested Capital)
- ROIIC (Return on Incremental Invested Capital)
- Reinvestment-Implied Growth
- WACC (derived via CAPM and capital structure inputs)
- FCFF (Free Cash Flow to the Firm)

The fundamental growth identity used is:
```
Growth = Reinvestment Rate × ROIIC
```

This ensures growth is earned through capital allocation, not assumed.

---

### 2. Intrinsic Valuation
- FCFF is discounted at WACC to estimate enterprise value
- Enterprise value is converted to equity value
- Equity value is converted to a price per share
- Conservative terminal assumptions are applied

This produces a fundamentals-driven intrinsic stock value.

---

### 3. Market-Implied Growth
Instead of forecasting growth, the model solves for it:

> *What growth rate must occur for intrinsic value to equal today’s market price?*

This reframes valuation as an expectations analysis, not a prediction exercise.

---

## Example Output (Apple)

### Derived Metrics (Annual)
```
            ROIC      ROIIC     Growth     WACC
2025-09-30  0.651319  2.127918  -0.035000  0.072799
2024-09-30  0.571784  0.408600  -0.035135  0.072633
2023-09-30  0.562689  -1.045343 -0.027863  0.072709
2022-09-30  0.586168  -0.311984  0.065481  0.072518
2021-09-30  0.490063        NaN       NaN       NaN
```

### Valuation Outputs
```
Market-Implied Growth: 18.72%
Intrinsic Stock Value: $104.29
Current Market Price: $273.40
```


---

## Important Clarification
All values shown above are derived by the model, except:

- Credit rating (used as an input to estimate cost of debt)
- Explicit 2025 anchor values used for normalization

Everything else (ROIC, ROIIC, growth, WACC, intrinsic value, and market-implied growth) is computed directly from financial statement data and valuation equations, not manually assumed.

---

## Interpretation
This result does not suggest Apple is a poor business. Instead, it highlights that:

- Apple is a high-quality, durable cash-flow generator
- The current price embeds very optimistic growth expectations
- Future returns depend more on expectation persistence than reinvestment-driven growth

The distinction between business quality and investment attractiveness is central to this framework.

---

## Why This Framework Is Useful
- Separates fundamentals from sentiment
- Avoids blind growth extrapolation
- Makes market expectations explicit

Works especially well for:
- Capital-light reinvestment businesses
- Mid-cap growth companies
- High-uncertainty or transitional firms

---

## Implementation
- Python-based
- Financial data sourced via yfinance
- Modular valuation engine for:
  - Fundamental growth
  - Intrinsic value
  - Market-implied growth
- Designed to be extended into screening and scenario analysis

---

## Motivation
This project was built as a learning exercise to apply investment theory rigorously, inspired by *Pitch the Perfect Investment*.

It focuses on clarity of expectations, not price targets or trading signals.

---

*Note: ChatGPT was used for implementation guidance and optimization support.*


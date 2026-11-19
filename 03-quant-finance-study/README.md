# Empirical Quantitative Finance Study

**Type:** Group project, MSc Financial Technology (Financial Analytics)
**My contribution:** [ADD YOUR PART HERE, e.g. "Led the Day 4 portfolio optimisation analysis and co-wrote Days 1 and 8"]

A series of empirical tests on how financial returns really behave, and what that means for forecasting, risk and portfolio choice. Data is downloaded with `yfinance` inside each notebook.

| Notebook | Question | Key finding |
|---|---|---|
| [`day1_return_distributions`](day1_return_distributions.ipynb) | Are gold and oil futures returns normally distributed? | No. Both reject normality (Shapiro-Wilk, KS); Student-t fits far better (≈4 and ≈6 degrees of freedom), and squared returns show volatility clustering |
| [`day2_arima_hsbc`](day2_arima_hsbc.ipynb) | Can ARIMA forecast HSBC's share price (1999–2002)? | The best model by AIC is ARIMA(0,1,0), the random walk: daily HSBC returns have no predictable linear pattern |
| [`day3_garch_volatility`](day3_garch_volatility.ipynb) | GARCH(1,1) or GJR-GARCH for FTSE 100, S&P 500 and Nikkei 225? | GJR-GARCH preferred on AIC/BIC for all three; it wins the forecast horserace on FTSE and Nikkei, GARCH on the S&P 500 |
| [`day4_mean_variance_portfolios`](day4_mean_variance_portfolios.ipynb) | Do optimised portfolios beat simple diversification out of sample? | No. Equal-weight (1/N) has the best Sharpe ratio (1.39); unconstrained mean-variance the worst (0.51) because estimation error is amplified |
| [`day5_capm_tests`](day5_capm_tests.ipynb) | Does the CAPM explain German stock returns? | Only 1 of 5 portfolios has a significant Jensen's alpha, but cross-sectional and Fama-MacBeth tests show CAPM struggles to explain returns |
| [`day8_portfolio_optimisation`](day8_portfolio_optimisation.ipynb) | Mean-variance vs Mean-VaR vs Mean-CVaR | Mean-CVaR gives the strongest out-of-sample risk-adjusted performance by managing tail risk |
| [`day9_factor_strategy`](day9_factor_strategy.ipynb) | Does a Value / Quality / Momentum / Low-Vol tilt beat 1/N on the Swiss SMI? | Yes, out of sample over 25 months: Sharpe 0.58 vs 0.50 with near-identical volatility, information ratio 1.30, outperforming in 17 of 25 months |

Days 6 (Fama-French 3-factor) and 7 (VaR / ES for the Nikkei 225) were also part of the study, but their notebooks are not included here.

## Run it

`pip install -r ../requirements.txt`, then run any notebook top to bottom.

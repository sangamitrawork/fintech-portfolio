# Tail-Risk Analysis of Wise plc After Anti-Money-Laundering Allegations

**Type:** Individual project, MSc Financial Technology (Financial Analytics)
**Notebook:** [`wise_tail_risk_analysis.ipynb`](wise_tail_risk_analysis.ipynb)

## Question

In 2026, Wise accounts were reported to have been used to launder about €500 million across Europe, and a Belgian prosecution was announced. Wise shares fell about 8% that day. **How much did the shock change Wise's downside risk, and which risk models capture it properly?**

## Approach

- Daily returns for Wise plc (WISE.L) from its July 2021 listing to December 2024, downloaded with `yfinance`
- Value-at-Risk (VaR) and Expected Shortfall (CVaR) at 5%, 2.5% and 1%, using 4 models: historical (non-parametric), Normal, Student-t and GARCH(1,1) with Student-t errors
- Bootstrap confidence intervals (5,000 resamples)
- Kupiec proportion-of-failures backtest over 627 rolling windows
- Event study of abnormal returns against a fintech-sector benchmark, ±10 trading days around the announcement
- Results framed against Basel III / FRTB requirements

## Key findings

- **The Normal model badly understates extreme losses.** At the 1% level, expected shortfall is 7.38% under the Normal model and 12.22% under Student-t, a 4.8-percentage-point gap that would leave a risk manager under-capitalised. Wise's returns are fat-tailed (kurtosis 5.22).
- **The shock persisted.** GARCH persistence of 0.963 implies a shock half-life of about 18 trading days, which a static VaR (flat at 4.08%) cannot capture.
- **Wise carries extra firm-specific risk.** VaR at 5% is 4.16%, against 3.90% for the fintech sector.
- **The market reacted on the announcement day only,** with no abnormal movement beforehand, consistent with no information leakage.
- **Backtesting:** the model passes Kupiec at the 1% level (p = 0.329). It fails at 5% and 2.5% because it is too *conservative*, not too risky, which reflects the IPO period and the shock itself in a short sample.

## Limitations

Daily public price data only, no intraday or options data; the sector benchmark excludes private UK fintechs such as Revolut and Monzo; estimates at the 1% level rest on few observations.

## Run it

`pip install -r ../requirements.txt`, then run the notebook top to bottom. Data downloads automatically.

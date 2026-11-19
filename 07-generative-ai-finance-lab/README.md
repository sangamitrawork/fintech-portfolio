# Generative AI in Finance: Lab Notebooks

**Type:** Individual weekly lab work, MSc Financial Technology (Generative AI)

Twelve short, hands-on experiments applying machine learning and generative AI to financial problems. Each notebook opens with a one-line summary.

## Reasoning and analysis with LLMs

| Notebook | What it does |
|---|---|
| [`coinbase_earnings_reasoning`](coinbase_earnings_reasoning.ipynb) | Tests whether Coinbase's revenue diversification is working, from its Q4 2023 earnings call, using structured prompting: atomic facts, chain-of-thought, tree-of-thought and role reversal |
| [`block_vs_paypal_10k_risk`](block_vs_paypal_10k_risk.ipynb) | Compares risk disclosures in Block's and PayPal's 2023 10-K filings, reading hedging language for latent risk |
| [`loan_amortisation_schedule`](loan_amortisation_schedule.ipynb) | Builds a calendar-accurate loan schedule (Actual/365, irregular payments) to check AI-generated financial calculations; final balance $87,838.10 |

## AI tools and agents

| Notebook | What it does |
|---|---|
| [`gemini_tool_calling_pe_ratio`](gemini_tool_calling_pe_ratio.ipynb) | Gives Gemini a live market-data tool (yfinance) and asks whether Apple looks overvalued on P/E |
| [`ai_agent_sharpe_ratios`](ai_agent_sharpe_ratios.ipynb) | An AI agent (smolagents) downloads prices and compares Sharpe ratios of tech and bank stocks *(code only)* |
| [`receipt_extraction_gemini_vision`](receipt_extraction_gemini_vision.ipynb) | Extracts totals from receipt images with Gemini's vision model and scores them against ground truth (CORD-v2 dataset) |
| [`visual_rag_financial_report`](visual_rag_financial_report.ipynb) | Visual RAG over a PDF financial report with LlamaIndex and the Qwen2.5-VL multimodal model *(code only, needs a GPU)* |
| [`financial_news_semantic_search`](financial_news_semantic_search.ipynb) | Semantic search over financial news with sentence embeddings and a Gradio interface |

## Machine learning for credit and fraud

| Notebook | What it does |
|---|---|
| [`credit_default_rf_xgboost_tabpfn`](credit_default_rf_xgboost_tabpfn.ipynb) | Credit-card default prediction: Random Forest vs XGBoost vs the TabPFN foundation model |
| [`credit_risk_mlp`](credit_risk_mlp.ipynb) | Credit-risk classification with a PyTorch neural network, from preprocessing to evaluation |
| [`complaint_classification_distilbert`](complaint_classification_distilbert.ipynb) | Fine-tunes DistilBERT to classify credit-card complaints by policy category and resolution *(code only, needs a GPU)* |
| [`synthetic_fraud_data_ctgan`](synthetic_fraud_data_ctgan.ipynb) | Generates synthetic fraud-transaction data with CTGAN; SDV quality score 0.68, discriminator AUC 0.71 |

*Code only* means the notebook was saved without outputs, so run it to see results. Notebooks that call Gemini read the key from Colab Secrets (`GEMINI_API_KEY`); no keys are stored here.

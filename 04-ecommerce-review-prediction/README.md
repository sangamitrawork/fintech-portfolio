# Predicting Positive Customer Reviews with LightGBM

**Type:** Group project, MSc Financial Technology (Big Data Analytics)
**My contribution:** [ADD YOUR PART HERE, e.g. "Feature engineering and leakage checks; threshold tuning; report writing"]
**Code:** written jointly with teammates and not published here; this page summarises the method and result.

## Question

Can an e-commerce platform predict, at the time an order is completed, whether the customer will leave a positive (4–5 star) review, so it can recognise satisfied customers early?

## Data

The public [Olist Brazilian e-commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (Kaggle): 8 linked tables covering orders, order items, customers, sellers, products, payments, reviews and geolocation.

## Approach

Followed the CRISP-DM process:
- merged the 8 tables into one order-level dataset, de-duplicating reviews and flagging missing geolocation
- **leakage-aware feature engineering:** only information available before the review is written
- appropriate train / test partitioning and class-imbalance handling
- LightGBM classifier, tuned for recall on the positive class, with decision-threshold optimisation

## Result

**0.96 recall and 0.88 F1** on positive reviews.


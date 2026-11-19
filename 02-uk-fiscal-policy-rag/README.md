# Verifiable AI for UK Fiscal Policy Research (RAG)

**Type:** Individual project, MSc Financial Technology (Generative AI)
**Notebooks:** [`baseline_rag.ipynb`](baseline_rag.ipynb) · [`enhanced_rag.ipynb`](enhanced_rag.ipynb)

## Question

General-purpose AI models are weak on specialist policy debate, and their answers are hard to check. **Can a retrieval-augmented system give answers on UK fiscal policy that are grounded in the source documents and traceable to the exact page?**

## Corpus

20 publications (1,061 pages, 4,201 text chunks) from the Office for Budget Responsibility and UK think tanks, including the IFS, NIESR, Resolution Foundation, Social Market Foundation, Institute for Government, Centre for Cities and New Economics Foundation. The PDFs are not included here for copyright reasons; all are publicly available from the publishers' websites.

## Approach

| | Baseline | Enhanced |
|---|---|---|
| Retrieval | Dense vector search (all-MiniLM-L6-v2 + FAISS) | **Hybrid**: dense + BM25 keyword search, merged with reciprocal rank fusion |
| Ranking | Similarity score only | **Cross-encoder reranking** (ms-marco-MiniLM-L-6-v2) |
| Chunking | 700-character chunks, 150 overlap, page-aware | 800-character chunks, 150 overlap, page-aware |
| Answers | Answer + page-level source list | Answer + **grounding note** (how well the evidence supports it) + page-level sources |
| Interface | — | Gradio chat app |

Answers are generated with Google Gemini.

## Evaluation and findings

Both systems were run on a 10-question test set covering 6 question types: factual, comparative, cross-document synthesis, evaluative, ambiguous and an edge case whose answer is not in the documents. Each answer was judged against expected-answer criteria written in advance.

- The enhanced system gave **better-grounded answers on all 10 questions**: it relied on retrieved evidence rather than fluent but unsupported synthesis.
- On the ambiguous question ("Is the UK in a strong fiscal position?") it gave a balanced, evidence-based answer where the baseline gave an overconfident verdict.
- On the edge case ("What is the exact GDP growth forecast for the UK in 2035?") it **declined to hallucinate** and said the documents do not contain that figure.
- Every answer cites its sources by document and page, so a researcher can verify it.

**Note on the metrics cells:** the notebook includes a precision@k / recall@k scaffold, but gold-standard chunk labels were not hand-labelled, so those cells show 0 / NaN. The automated LLM-judge cell scored both systems 5/5 on a small sample, which did not separate them. The comparison above comes from manual, criteria-based review.

## Limitations

Hand-curated corpus, so not yet scalable; source-selection and retrieval bias are possible; retrieval can still miss content phrased in unusual terminology or spread across sections.

## Run it

Runs in Google Colab. Add a `GEMINI_API_KEY` in Colab Secrets, download the PDFs, zip them as `fiscal_policy_pdfs.zip` and upload it to Colab, then run top to bottom.

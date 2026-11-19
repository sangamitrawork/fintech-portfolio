# Multi-LLM, Human-in-the-Loop Capital Budgeting

**Type:** Group project, MSc Financial Technology (Generative AI)
**My contribution:** Worked across the full project as a team member: designing the multi-model pipeline and prompts, evaluating the AI outputs against the rubric and writing the reflection.
**Code:** [`multi_llm_pipeline.py`](multi_llm_pipeline.py)

## Question

Can generative AI produce a board-level capital-budgeting recommendation that a finance professional could trust, and where does it fail?

## Task

A professional task from OpenAI's GDPval benchmark: a Senior Finance Manager must evaluate two proposals, a $50M emerging-market expansion and a $40M R&D project, against a $100M cash position and a 9% WACC.

## Approach

A four-stage pipeline across several AI providers (Google Gemini, OpenAI, Anthropic Claude, and Llama via Hugging Face):
1. **Context injection:** task documents fed in with explicit constraints, e.g. "avoid fabricated data"
2. **Structured prompting:** Role-Task-Framework prompts and step-by-step decomposition
3. **Cross-model validation:** one model grades another's report against the GDPval rubric
4. **Human review:** reconciling disagreements and correcting hallucinated claims

Outputs were scored on a five-part rubric: correctness, completeness, analytical depth, clarity and usefulness.

## Findings

- **Cross-model checking works.** OpenAI's review of Gemini's first report caught missing cash-flow logic, no risk-adjusted discounting and no opportunity-cost analysis, which forced substantive revision.
- **Financial hallucination is real.** One model claimed a project had a negative risk-adjusted NPV and an IRR of 15–20%, which is impossible when the WACC is 9%.
- **Humans still add judgement.** No model suggested keeping a liquidity reserve; a human added a $10M buffer.
- **There is a depth ceiling.** Models stayed qualitative ("NPV is likely positive") rather than building sensitivity or scenario analysis.

## Run it

Set any of `GEMINI_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GROQ_API_KEY` or `HF_API_KEY` as environment variables (no keys are stored in the code), install the libraries in `../requirements.txt`, and run the script in a notebook environment such as Colab.

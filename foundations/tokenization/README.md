## Tokenization Experiments

These experiments follow the tokenization material in Raschka, Chapter 2, and examine how general-purpose language-model tokenizers represent biomedical terminology.

How are gene symbols, protein mutation identifiers, punctuation, and scientific terms split into tokens by different generations of byte-pair encoding (BPE) tokenizers?

The notebook [`01_tokenization_experiments.ipynb`](01_tokenization_experiments.ipynb) uses `tiktoken` to compare:

- `gpt2`: approximately 50K tokens
- `cl100k_base`: approximately 100K tokens, used by GPT-3.5/GPT-4-era models
- `o200k_base`: approximately 200K tokens, used by later models

The test phrases include:

- General medical text
- Gene symbols such as `EGFR`, `BRCA1`, `BRCA2`, `TP53`, and `KRAS`
- Mutation identifiers such as `T790M`, `p.T790M`, and `G12D`
- Punctuation-heavy biomedical text
- `CRISPR-Cas9 genome editing`

For each tokenizer and phrase, I print the token count and render it as an HTML visualization. Each colored token box shows the decoded token and its integer token ID; spaces and newlines are displayed as `␣` and `↵` to make invisible characters explicit.

### Generated visualization

![Tokenization comparison across tokenizer vocabularies](tokenization_comparison.svg)

In this sample, the newer encodings are modestly more token-efficient: `gpt2` uses 82 tokens across the five rendered phrases, while both `cl100k_base` and `o200k_base` use 75, an approximately 8.5% reduction. The improvement is not universal: some phrases have the same count across all three encodings. Here, efficiency means representing the same text with fewer tokens, which can reduce context-window usage and the compute or cost associated with processing a prompt. It does not by itself imply better biomedical understanding.

Gene symbols and mutation notation may still be represented as several subword tokens rather than as single semantic units, and small changes in punctuation or formatting can change the resulting tokenization. This makes token counts useful when estimating context usage for biomedical datasets.
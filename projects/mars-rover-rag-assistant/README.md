# Mars Rover Research Assistant

**GitHub source:** [View code and project documentation](https://github.com/harshV264/harshV264/tree/main/projects/mars-rover-rag-assistant)

A local Retrieval-Augmented Generation (RAG) prototype that answers questions from NASA Mars rover technical reports and displays the passages used as evidence. Answers are not guaranteed to be correct; citations let readers verify them.

## Sources

NASA Technical Reports Server records used by the downloader:

- [A conceptual design and operational characteristics for a Mars rover for a 1979 or 1981 Viking science mission](https://ntrs.nasa.gov/citations/19740009428) — NASA-TN-D-7462; record lists public-use permission.
- [United States planetary rover status: 1989](https://ntrs.nasa.gov/citations/19900016037) — NASA-CR-186843; record lists public-use permission.
- [A Long Range Science Rover For Future Mars Missions](https://ntrs.nasa.gov/citations/20010000521) — URC97163; NASA's record lists the document as a U.S. Government work with public-use permission.

NASA NTRS provides public records and documents subject to its [disclaimers, copyright notice, and terms of use](https://sti.nasa.gov/disclaimers/). The project stores report metadata and citations. The downloaded PDFs remain local and are not included in Git.

## Stack

- Python, pypdf, Sentence Transformers (`multi-qa-MiniLM-L6-dot-v1`), NumPy exact vector search, BM25 retrieval, and a Sentence Transformers cross-encoder.
- Ollama with `qwen3:1.7b` for local answer generation. No hosted LLM API key is required.
- Streamlit for the local demo.

The corpus is small enough for exact local vector search, so the index stores vectors in a NumPy file and passage metadata in JSON rather than requiring a database server. Choose semantic-only or hybrid BM25-plus-semantic retrieval; optional cross-encoder reranking is available as a third mode. The embedding and answer models download on first use; after that, the app runs locally.

## Setup (Windows PowerShell)

From this folder:

```powershell
py -3.10 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Install Ollama from its official site, then download the local answer model once. Ollama is required for answer generation; report retrieval and evidence display are evaluated separately.

```powershell
ollama pull qwen3:1.7b
```

Download the reports and build the local index:

```powershell
python scripts\download_reports.py
python scripts\build_index.py
python scripts\evaluate_retrieval.py
streamlit run app.py
```

## Evaluation

The eight hand-written questions in `evaluation/questions.csv` target report pages verified during corpus inspection. On this small benchmark, semantic-only retrieval found the expected source and page in 5/8 top-five results (Recall@5 **0.625**, mean query time **0.058 s**); hybrid retrieval found 8/8 (Recall@5 **1.000**, mean **0.063 s**). Detailed per-query results are saved to `evaluation/retrieval_results.json` by `python scripts/evaluate_retrieval.py`. Times were measured locally on an RTX 3050 Laptop GPU system after loading the embedding model; they are machine-dependent and do not include answer generation.

This benchmark measures whether a matching source/page appears in the top five; it does not prove the generated answer is correct or fully supported. Review answer citations manually and expand the benchmark before making strong quality claims.

## Limitations

- The corpus is intentionally small and focused on rover design; answers are limited to the indexed reports.
- PDF text extraction can lose layout or return little text for scanned pages. Check extracted text before relying on the index.
- Small local language models can miss evidence or produce unsupported answers. Verify citations against the source.
- Report coverage is not representative of all Mars research.
- NASA reports are scientific/technical source material; this demo is not an official NASA product.



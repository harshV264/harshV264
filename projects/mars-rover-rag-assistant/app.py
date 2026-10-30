from pathlib import Path
import sys
import time

import streamlit as st

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from rag_assistant.pipeline import answer_question, retrieve  # noqa: E402

st.set_page_config(page_title="Mars Rover Research Assistant", page_icon="🪐", layout="wide")
st.title("Mars Rover Research Assistant")
st.caption("A local, citation-first RAG prototype over selected NASA technical reports.")
st.info("Research aid only. Verify important facts against the cited NASA report and page.")

question = st.text_area("Ask a question about the indexed reports", placeholder="How did early Mars rover designs handle mobility?")
strategy = st.selectbox("Retrieval method", ["hybrid", "dense", "hybrid-rerank"], format_func=lambda value: {
    "hybrid": "Hybrid (semantic + keyword)",
    "dense": "Semantic only",
    "hybrid-rerank": "Hybrid + cross-encoder reranking (downloads a model on first use)",
}[value])

if st.button("Search reports", type="primary", disabled=not question.strip()):
    try:
        start = time.perf_counter()
        with st.spinner("Retrieving passages and generating a local answer…"):
            passages = retrieve(question, top_k=5, strategy=strategy)
            retrieval_done = time.perf_counter()
            try:
                answer = answer_question(question, passages)
            except Exception as exc:
                answer = (
                    "Local answer generation is unavailable. The retrieved evidence is still shown below. "
                    "Install and start Ollama, then pull qwen3:1.7b to enable answers.\n\n"
                    f"Details: {exc}"
                )
            finished = time.perf_counter()
        st.session_state["rag_result"] = {
            "answer": answer,
            "passages": passages,
            "retrieval_seconds": retrieval_done - start,
            "generation_seconds": finished - retrieval_done,
        }
    except Exception as exc:
        st.error(str(exc))

result = st.session_state.get("rag_result")
if result:
    st.subheader("Answer")
    st.write(result["answer"])
    col1, col2 = st.columns(2)
    col1.metric("Retrieval time", f"{result['retrieval_seconds']:.2f}s")
    col2.metric("Local generation time", f"{result['generation_seconds']:.2f}s")
    with st.expander("Retrieved evidence"):
        for index, item in enumerate(result["passages"], start=1):
            st.markdown(f"**[{index}] {item['source']} · page {item['page']}**")
            st.write(item["text"])

st.divider()
st.caption("The source PDFs and local index are not uploaded or included in this repository.")



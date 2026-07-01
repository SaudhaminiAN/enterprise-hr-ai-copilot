import os
import sys
import time

import streamlit as st

# =====================================================
# Add src folder to Python path
# =====================================================

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "src"
        )
    )
)

from hr_copilot import ask_hr_copilot
from build_knowledge_base import build_knowledge_base

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Enterprise HR AI Copilot",
    page_icon="🤖",
    layout="wide"
)

# =====================================================
# Sidebar
# =====================================================

with st.sidebar:

    st.title("🤖 HR AI Copilot")

    st.markdown("---")

    st.subheader("🚀 Powered By")

    st.success("Gemini 2.5 Flash")
    st.success("Sentence Transformers")
    st.success("ChromaDB")

    st.markdown("---")

    st.subheader("💡 Example Questions")

    st.write("• How many casual leaves are allowed?")
    st.write("• How many sick leaves are allowed?")
    st.write("• Can I work from home?")
    st.write("• What is the travel reimbursement policy?")
    st.write("• What is the attendance policy?")

    st.markdown("---")

    # =====================================================
    # Upload PDF
    # =====================================================

    st.subheader("📂 Upload HR Policy")

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        st.info(f"Selected: {uploaded_file.name}")

        if st.button(
            "📤 Upload PDF",
            use_container_width=True
        ):

            os.makedirs("data", exist_ok=True)

            save_path = os.path.join(
                "data",
                uploaded_file.name
            )

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner(
                "Updating ChromaDB..."
            ):

                total_chunks = build_knowledge_base()

            st.success(
                f"""
✅ {uploaded_file.name} uploaded successfully!

Knowledge Base Updated Successfully!

Indexed {total_chunks} chunks.
"""
            )

    st.markdown("---")

    st.caption("Enterprise HR AI Copilot v3.0")

# =====================================================
# Main Page
# =====================================================

st.title("🏢 Enterprise HR AI Copilot")

st.caption(
    "AI-powered HR Policy Assistant using Retrieval-Augmented Generation (RAG)"
)

st.divider()

question = st.text_area(
    "Ask your HR Question",
    placeholder="Example: How many casual leaves are allowed?",
    height=120
)

ask = st.button(
    "🔍 Ask HR Copilot",
    use_container_width=True
)

# =====================================================
# Ask Question
# =====================================================

if ask:

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        start_time = time.time()

        with st.spinner(
            "Searching HR policies..."
        ):

            response = ask_hr_copilot(question)

        elapsed = time.time() - start_time

        # =====================================================
        # Answer
        # =====================================================

        st.success("Answer")

        st.markdown(response["answer"])

        st.divider()

        # =====================================================
        # Sources
        # =====================================================

        st.subheader("📄 Sources Used")

        for i, source in enumerate(
            response["sources"],
            start=1
        ):

            title = (
                f"Source {i}: "
                f"{source['source']} "
                f"(Page {source['page']})"
            )

            with st.expander(title):

                if "score" in source:

                    st.write(
                        f"**Similarity Score:** {source['score']:.4f}"
                    )

                st.write(source["content"])

        st.divider()

        # =====================================================
        # Metrics
        # =====================================================

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "⏱ Response Time",
                f"{elapsed:.2f} sec"
            )

        with col2:

            st.metric(
                "🤖 LLM",
                "Gemini 2.5 Flash"
            )

        with col3:

            st.metric(
                "🗄 Vector DB",
                "ChromaDB"
            )
import streamlit as st
import requests

st.set_page_config(
    page_title="Second Brain",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Second Brain - Personal Knowledge Management System")

# -----------------------------
# Upload PDF
# -----------------------------

st.header("📄 Upload PDF")

uploaded_file = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)

if uploaded_file is not None:

    if st.button("Upload PDF"):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        response = requests.post(
            "http://127.0.0.1:8000/upload",
            files=files
        )

        if response.status_code == 200:

            st.success("✅ PDF Uploaded Successfully")

            # -----------------------------
            # Document Statistics
            # -----------------------------

            stats = requests.get(
                "http://127.0.0.1:8000/document-info"
            ).json()

            st.subheader("📊 Document Statistics")

            st.write("📄 Filename :", stats.get("filename"))
            st.write("🔤 Characters :", stats.get("characters"))
            st.write("📝 Words :", stats.get("words"))
            st.write("🧩 Chunks :", stats.get("chunks"))
            st.write(
                "⏱ Estimated Reading Time :",
                str(stats.get("estimated_reading_time")) + " min"
            )

            # -----------------------------
            # Document Summary
            # -----------------------------

            summary = requests.get(
                "http://127.0.0.1:8000/document-summary"
            ).json()

            st.subheader("📋 Document Summary")

            st.write("📄 Filename :", summary.get("filename"))

            st.write(
                "📖 Estimated Reading Time :",
                str(summary.get("reading_time")) + " min"
            )

            st.write("📌 Main Topics")

            topics = summary.get("topics", [])

            if topics:
                for topic in topics:
                    st.write("•", topic)
            else:
                st.write("No topics detected.")

        else:

            st.error("❌ Upload Failed")

# -----------------------------
# Ask Question (Beta)
# -----------------------------
st.header("🔍 Keyword Search")

keyword = st.text_input(
    "Enter Keyword"
)

if st.button("Search Keyword"):

    response = requests.post(

        "http://127.0.0.1:8000/keyword-search",

        json={
            "keyword": keyword
        }

    )

    if response.status_code == 200:

        data = response.json()

        st.success(
            f"Found {data['count']} matches"
        )

        for result in data["results"]:

            st.write("📌", result)

    else:

        st.error("Search Failed")

st.header("❓ Ask Question (Beta)")

question = st.text_input("Enter your question")

if st.button("Ask"):

    response = requests.post(
        "http://127.0.0.1:8000/ask",
        json={"question": question}
    )

    if response.status_code == 200:

        result = response.json()

        st.success("✅ Answer Generated")

        st.subheader("📄 Retrieved Answer")

        st.write(result["answer"])


    else:

        st.error("❌ Backend Error")




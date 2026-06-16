from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from pypdf import PdfReader
import chromadb
import os


# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI()

# -----------------------------
# Create uploads folder
# -----------------------------
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# -----------------------------
# Initialize ChromaDB
# -----------------------------
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_or_create_collection(
    name="documents"
)

# -----------------------------
# Request Model
# -----------------------------
class QuestionRequest(BaseModel):
    question: str
class KeywordRequest(BaseModel):
    keyword: str

# -----------------------------
# Home Route
# -----------------------------
document_info = {}
document_summary = {}
document_text = ""
@app.get("/")
def home():
    return {
        "message": "Second Brain Backend Running"
    }

# -----------------------------
# Upload PDF
# -----------------------------
@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):

    # Save PDF
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Read PDF
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    text = text.replace("\n", " ")
    global document_text
    document_text = text

    # Split into chunks
    chunk_size = 200

    chunks = [
        text[i:i + chunk_size]
        for i in range(0, len(text), chunk_size)
    ]

    # Delete old documents
    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])

    # Store in ChromaDB
    collection.add(
        documents=chunks,
        ids=[f"{file.filename}_{i}" for i in range(len(chunks))]
    )

    # Store document statistics
    words = text.split()

    document_info["filename"] = file.filename
    document_info["characters"] = len(text)
    document_info["words"] = len(words)
    document_info["chunks"] = len(chunks)
    document_info["estimated_reading_time"] = max(1, len(words) // 200)
    topics = []

    text_lower = text.lower()

    if "education" in text_lower:
        topics.append("Education")

    if "skills" in text_lower:
        topics.append("Skills")

    if "projects" in text_lower:
        topics.append("Projects")
    if "certification" in text_lower or "certifications" in text_lower:
        topics.append("Certifications")
    if "experience" in text_lower:
        topics.append("Experience")

    document_summary["filename"] = file.filename
    document_summary["reading_time"] = max(1, len(words)//200)
    document_summary["topics"] = topics



    return {
        "filename": file.filename,
        "characters_extracted": len(text),
        "total_chunks": len(chunks),
        "stored_in_chromadb": True
    }
@app.get("/document-info")
async def get_document_info():

    return document_info
@app.get("/document-summary")
async def get_document_summary():

    return document_summary



# -----------------------------
# Ask Question
# -----------------------------
@app.post("/ask")
async def ask_question(request: QuestionRequest):


    # Retrieve top 5 relevant chunks
    results = collection.query(
        query_texts=[request.question],
        n_results=1
    )

    retrieved_docs = results["documents"][0]
    print("\n====================")
    print("Retrieved Chunks:")
    print(retrieved_docs)
    print("====================\n")
    answer = retrieved_docs[0]

    return {
        "question": request.question,
        "answer": answer
    }
@app.post("/keyword-search")
async def keyword_search(request: KeywordRequest):

    keyword = request.keyword.strip().lower()

    text = document_text.lower()

    results = []

    start = 0

    while True:

        index = text.find(keyword, start)

        if index == -1:
            break

        snippet_start = max(0, index - 60)
        snippet_end = min(len(document_text), index + len(keyword) + 80)

        results.append(document_text[snippet_start:snippet_end])

        start = index + len(keyword)

    return {
        "keyword": request.keyword,
        "count": len(results),
        "results": results[:5]
    }
# 🧠 Second Brain - Personal Knowledge Management System

A decoupled full-stack AI-native document intelligence platform that allows users to upload PDF documents, extract underlying content metrics, search text via key-phrases, and run semantic vector-space queries over unstructured data.

## 📸 App Interface & Dashboard
<!-- DRAG AND DROP YOUR SCREENSHOT DIRECTLY ON THE LINE BELOW -->
<img width="1757" height="556" alt="Screenshot 2026-06-16 181604" src="https://github.com/user-attachments/assets/1eb54beb-3014-4a96-9f0e-381618291413" />
<img width="1712" height="892" alt="Screenshot 2026-06-16 181622" src="https://github.com/user-attachments/assets/dd7a80a2-1151-4a9c-a9cd-374e22003932" />
<img width="1752" height="597" alt="Screenshot 2026-06-16 181631" src="https://github.com/user-attachments/assets/b50326c5-083a-408b-8936-1f9783164c3e" />





## 🏗️ Architecture Layout
The application is structured into a separated microservices architecture:
- **Backend (`FastAPI`):** Handles multi-page parsing, token block chunking, and local vector search updates.
- **Frontend (`Streamlit`):** Provides a visual file uploading system, statistical analysis readouts, and search consoles.

## ✨ Core Features
- **Document Ingestion:** Automated binary text extraction and dynamic categorical classification (Education, Skills, Projects, etc.).
- **Vector Embeddings Database:** Integrates local on-disk persistence via ChromaDB for semantic-level chunk search operations.
- **Asynchronous Search Engines:** Features concurrent sub-string pattern searching alongside vector-distance querying.

## 🛠️ Built With
- **FastAPI** - High-performance backend REST API framework
- **Streamlit** - Rapid front-end user experience layout
- **ChromaDB** - Local Open-Source AI Vector Database
- **PyPDF** - Document processing and structural extraction layer

# RFI Document Summarizer & Chatbot

A modular, Python-based Gradio app for **summarizing RFI (Request for Information) documents** and providing an **interactive chatbot** for Q&A—powered by your choice of LLMs (Llama 3.2, GPT-4o mini, DeepSeek, etc.).  
Built for fund managers, analysts, and anyone who needs to extract and explore insights from complex PDF documents.

---

## ✨ Features

- **Upload and summarize** RFI PDFs into key sections: Price, People, Philosophy, Process, Performance
- **Download styled DOCX** summaries, ready for presentation and sharing
- **Chatbot interface**: Ask questions about the document and get instant, context-aware answers
- **Supports multiple LLMs**: Llama 3.2 (local), GPT-4o mini (API), DeepSeek-chat(API)
- **Modern Gradio UI** with dark mode, progress indicators, and keyboard shortcuts
- **Secure**: `.env` is excluded from Git for API key safety

---

## 🚀 Demo Screenshots

### 1. Welcome Screen

![Screen 1](https://github.com/user-attachments/assets/6625c0c1-b010-4b8a-b141-7687a65b517a)

### 1.1 Import the RFI document

![Screen 2 - import pdf](https://github.com/user-attachments/assets/84429987-045c-4245-a4a9-fb53d3ce8703)


---

### 2. Summarization Output

- Upload your RFI PDF and select your preferred LLM.
- Click **Summarize** to generate structured section summaries.


![Screen 3 - output of summary](https://github.com/user-attachments/assets/e8bb77c9-d06d-4a5b-af0e-cd6e9617fb52)

---

### 3. Chatbot: Document Loading

- Upload your document in the **Chatbot** tab.
- See a clear loading status while embeddings and context are prepared.

![Screen 4 - chatbot](https://github.com/user-attachments/assets/1efdbb28-2052-4a91-a951-467cee211aaa)


---

### 4. Chatbot: Q&A Example

- Ask natural language questions about the uploaded document.
- Get accurate, context-rich answers instantly.

![Screen 5 - chatbot output](https://github.com/user-attachments/assets/5514a949-ed1c-4334-b2e6-b66b5efb0cf7)


---

## 🛠️ How to Run

1. **Clone this repo**
2. **Install Python 3.9+ and [Git](https://git-scm.com/)**
3. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```
4. **Set up your `.env`** (for OpenAI/DeepSeek API keys; local models do not require keys)
5. **Launch the app:**
    ```
    python app.py
    ```
6. **Open the local Gradio URL** in your browser

---

## ⚡ Usage Tips

- **Summarization**: Upload a PDF, select LLM, click Summarize, and download the styled DOCX.
- **Chatbot**: Upload a PDF, wait for "Document loaded" status, then ask questions using the Send button or press Enter.
- **API keys**: Never upload your `.env` to GitHub—it's already excluded via `.gitignore`.

---

## 📝 Project Structure

.
├── app.py
├── llm_manager.py
├── summarizer.py
├── embedder.py
├── chatbot.py
├── docx_generator.py
├── requirements.txt
├── .env # (excluded from Git)
└── README.md


---

## 🔒 Security

- **API keys** are stored in `.env` and excluded from GitHub via `.gitignore`.

---

## 📄 License

MIT License.  
See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- Built with [Gradio](https://gradio.app/), [python-docx](https://python-docx.readthedocs.io/), and open-source LLMs.
- Screenshots and UI design inspired by modern document AI workflows.

---


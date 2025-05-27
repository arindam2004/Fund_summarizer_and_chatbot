import PyPDF2

SECTION_PROMPTS = {
    "Price":      "Summarize the RFI document with a focus on pricing, fees, and cost-related information.",
    "People":     "Summarize the RFI document with a focus on the people involved, team structure, and key personnel.",
    "Philosophy": "Summarize the RFI document with a focus on investment philosophy and guiding principles.",
    "Process":    "Summarize the RFI document with a focus on investment process, methodology, and workflow.",
    "Performance":"Summarize the RFI document with a focus on historical and recent performance metrics and results."
}

def pdf_to_chunks(pdf_path, chunk_size=1500, overlap=300):
    reader = PyPDF2.PdfReader(pdf_path)
    text = " ".join(page.extract_text() for page in reader.pages if page.extract_text())
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i+chunk_size])
    return chunks

def summarize_document(chunks, llm_manager):
    section_summaries = {}
    full_text = "\n".join(chunks)
    for section, prompt in SECTION_PROMPTS.items():
        full_prompt = f"{prompt}\n\nDocument Text:\n{full_text}\n\nProvide a concise summary for the '{section}' section."
        summary = llm_manager.generate(full_prompt)
        section_summaries[section] = summary.strip()
    return section_summaries

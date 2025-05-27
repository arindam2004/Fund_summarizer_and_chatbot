import gradio as gr

from llm_manager import LLMManager
from summarizer import pdf_to_chunks, summarize_document
from embedder import Embedder
from chatbot import Chatbot
from docx_generator import generate_summary_docx

def summarize_rfi(pdf_file, model_choice):
    llm = LLMManager(model_name=model_choice)
    chunks = pdf_to_chunks(pdf_file)
    section_summaries = summarize_document(chunks, llm)
    return section_summaries

def handle_summary_download(pdf_file, model_choice):
    llm = LLMManager(model_name=model_choice)
    chunks = pdf_to_chunks(pdf_file)
    section_summaries = summarize_document(chunks, llm)
    docx_path = generate_summary_docx(section_summaries)
    return docx_path

def chatbot_interface(pdf_file, model_choice):
    llm = LLMManager(model_name=model_choice)
    embedder = Embedder()
    chunks = pdf_to_chunks(pdf_file)
    bot = Chatbot(chunks, embedder, llm)
    return bot

with gr.Blocks() as demo:
    gr.Markdown("# RFI Document Summarizer & Chatbot")

    with gr.Tab("Summarization"):
        pdf_input = gr.File(label="Upload RFI PDF", type="filepath")
        model_dropdown = gr.Dropdown(
            choices=["llama-3.2", "gpt-4o-mini", "deepseek-chat"],
            value="llama-3.2",
            label="Select LLM"
        )
        summary_output = gr.JSON(label="Section Summaries")
        summarize_btn = gr.Button("Summarize")
        download_btn = gr.Button("Download Styled Summary DOCX")
        download_output = gr.File(label="Download Summary")

        summarize_btn.click(
            summarize_rfi,
            inputs=[pdf_input, model_dropdown],
            outputs=summary_output
        )

        download_btn.click(
            handle_summary_download,
            inputs=[pdf_input, model_dropdown],
            outputs=download_output
        )

    with gr.Tab("Chatbot"):
        pdf_input_chat = gr.File(label="Upload RFI PDF for Chat", type="filepath")
        model_dropdown_chat = gr.Dropdown(
            choices=["llama-3.2", "gpt-4o-mini", "deepseek-chat"],
            value="llama-3.2",
            label="Select LLM"
        )
        chatbot_state = gr.State()
        load_status = gr.Markdown("**Status:** No document loaded.")
        chatbot_ui = gr.Chatbot(label="Ask about the RFI document", type="messages")
        user_input = gr.Textbox(label="Your question", show_label=True)
        send_btn = gr.Button("Send")

        def show_loading_message(file, model):
            return None, "**Status:** Loading document... Please wait."

        def init_chatbot(pdf_file, model_choice):
            try:
                bot = chatbot_interface(pdf_file, model_choice)
                return bot, "**Status:** Document loaded successfully. You can now ask questions."
            except Exception as e:
                print(f"Error initializing chatbot: {e}")
                return None, f"**Status:** Error loading document: {e}"

        def chat_with_doc(user_msg, chatbot_state):
            if chatbot_state is None:
                return [{"role": "assistant", "content": "Chatbot is not initialized. Please check your document and try again."}], chatbot_state, ""
            response = chatbot_state.chat(user_msg)
            return chatbot_state.history, chatbot_state, ""

        # Show loading message as soon as file is selected
        pdf_input_chat.change(
            show_loading_message,
            inputs=[pdf_input_chat, model_dropdown_chat],
            outputs=[chatbot_state, load_status],
            queue=False
        )
        # Actually load the chatbot (with progress bar)
        pdf_input_chat.change(
            init_chatbot,
            inputs=[pdf_input_chat, model_dropdown_chat],
            outputs=[chatbot_state, load_status],
            show_progress=True
        )

        # Both Send button and Enter key trigger chat, and clear the input box after sending
        send_btn.click(
            chat_with_doc,
            inputs=[user_input, chatbot_state],
            outputs=[chatbot_ui, chatbot_state, user_input]
        )
        user_input.submit(
            chat_with_doc,
            inputs=[user_input, chatbot_state],
            outputs=[chatbot_ui, chatbot_state, user_input]
        )

demo.launch(share=True)

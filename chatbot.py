from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Chatbot:
    def __init__(self, chunks, embedder, llm_manager):
        self.chunks = chunks
        self.embedder = embedder
        self.llm_manager = llm_manager
        self.chunk_embeddings = np.array(embedder.get_embeddings(chunks))
        self.history = []

    def retrieve(self, query, top_k=3):
        query_emb = np.array(self.embedder.get_embeddings([query], task_type="search_query"))[0]
        sims = cosine_similarity([query_emb], self.chunk_embeddings)[0]
        top_indices = sims.argsort()[-top_k:][::-1]
        return [self.chunks[i] for i in top_indices]

    def chat(self, query):
        context_chunks = self.retrieve(query)
        context = "\n\n".join(context_chunks)
        prompt = f"Given the following context from the RFI document:\n{context}\n\nAnswer the user's question: {query}"
        response = self.llm_manager.generate(prompt)
        # Append as dicts, not tuples!
        self.history.append({"role": "user", "content": query})
        self.history.append({"role": "assistant", "content": response})
        return response


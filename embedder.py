# Uses local Nomic Embed Text model, no API key needed
from nomic import embed

class Embedder:
    def __init__(self, model="nomic-embed-text-v1.5"):
        self.model = model

    def get_embeddings(self, texts, task_type="search_document"):
        return embed.text(
            texts=texts,
            model=self.model,
            task_type=task_type,
            inference_mode='local',
            dimensionality=768
        )["embeddings"]

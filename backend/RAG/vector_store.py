from langchain_core.vectorstores import VectorStore
from langchain.embeddings import Embeddings
from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document

class HuggingFaceEmbeddings(Embeddings):
    """A wrapper around HuggingFace embeddings."""

    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def embed_documents(self, documents: list[str]) -> list[list[float]]:
        """Embed a list of documents."""
        return self.model.encode(documents).tolist()

    def embed_query(self, query: str) -> list[float]:
        """Embed a query."""
        return self.model.encode([query])[0].tolist()
    

class InMemoryVectorStore(VectorStore):
    """An in-memory vector store."""

    def __init__(self, embeddings: Embeddings):
        self._embeddings = embeddings
        self.vectors = []
        self.documents = []

    def add_documents(self, documents: list[Document]):
        """Add documents to the vector store."""
        self.documents.extend(documents)
        document_texts = [doc.page_content for doc in documents]
        self.vectors.extend(self._embeddings.embed_documents(document_texts))

    def remove_document(self, document_ids: str):
        """Remove document from the vector store."""
        indices_to_remove = [i for i, doc in enumerate(self.documents) if doc.metadata["id"] == document_ids]
        
        self.documents = [doc for i, doc in enumerate(self.documents) if i not in indices_to_remove]
        self.vectors = [vec for i, vec in enumerate(self.vectors) if i not in indices_to_remove]

    def from_texts(self, texts: list[str], metadatas: list[dict]) -> list[Document]:
        """Create documents from texts and metadatas."""
        documents = [Document(page_content=text, metadata=metadata) for text, metadata in zip(texts, metadatas)]
        self.add_documents(documents)
        return documents
    

    def similarity_search(self, query: str, k: int = 4) -> list[str]:
        """Perform a similarity search."""
        query_vector = self._embeddings.embed_query(query)
        similarities = [self.cosine_similarity(query_vector, vector) for vector in self.vectors]
        top_k_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)[:k]
        return [self.documents[i] for i in top_k_indices]

    @staticmethod
    def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
        """Calculate the cosine similarity between two vectors."""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm_vec1 = sum(a * a for a in vec1) ** 0.5
        norm_vec2 = sum(b * b for b in vec2) ** 0.5
        if norm_vec1 == 0 or norm_vec2 == 0:
            return 0.0
        return dot_product / (norm_vec1 * norm_vec2)
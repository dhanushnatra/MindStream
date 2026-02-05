from pathlib import Path
from langchain_core.documents import Document
from langchain_core.document_loaders import BaseLoader
from RAG.vector_store import HuggingFaceEmbeddings, InMemoryVectorStore
from RAG.text_reader import load_and_split

embeddings=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

vector_store = InMemoryVectorStore(embeddings=embeddings)



class DocLoader(BaseLoader):
    """A document loader that loads documents from a list of strings | file paths."""

    def __init__(self, file_paths: list[str|Path]):
        self.file_paths = file_paths

    def load(self) -> list[Document]:
        """Load the documents."""
        documents = []
        for file_path in self.file_paths:
            splits = load_and_split(file_path)
            for split in splits:
                vector_store.add_documents([Document(page_content=split, metadata={"source": str(file_path), "id": f"{file_path}_{len(vector_store.documents)}"})])
        return documents
    
    def remove_file(self, file_path: str|Path):
        """Remove a file from the loader."""
        self.file_paths.remove(file_path)
        vector_store.remove_document(str(file_path))

    def add_file(self, file_path: str|Path):
        """Add a file to the loader."""
        self.file_paths.append(file_path)
        splits = load_and_split(file_path)
        for split in splits:
            vector_store.add_documents([Document(page_content=split, metadata={"source": str(file_path), "id": f"{file_path}_{len(vector_store.documents)}"})])
    
    def similarity_search(self, query: str, k: int = 4) -> tuple[list[Document],int]:
        """Perform a similarity search."""
        return vector_store.similarity_search(query, k=k),k
from pathlib import Path
from RAG.doc_loader import DocLoader

class Retriever:
    """A retriever class to manage document loading and similarity search."""
    def __init__(self):
        self.file_paths:list[Path] = []
        self.doc_loader = DocLoader(file_paths=self.file_paths)

    def add_file(self, file_path: str|Path):
        """Add a file to the document loader."""
        self.doc_loader.add_file(file_path)
        self.file_paths.append(Path(file_path))

    def remove_file(self, file_path: str|Path):
        """Remove a file from the document loader."""
        self.doc_loader.remove_file(file_path)
        self.file_paths.remove(Path(file_path))

    def get_similar_from_query(self, query: str, k: int = 4):
        """Get similar documents from a query."""
        return self.doc_loader.similarity_search(query, k=k)
import os
from pathlib import Path
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class PDFRetriever:
    def __init__(self, pdf_directory: str):
        self.pdf_directory = pdf_directory
        self.documents = []
        self.vectorizer = TfidfVectorizer(max_features=500)
        self.tfidf_matrix = None
        self.load_pdfs()
    
    def load_pdfs(self):
        """Load and extract text from all PDFs in directory."""
        pdf_files = list(Path(self.pdf_directory).glob("*.pdf"))
        for pdf_file in pdf_files:
            try:
                with open(pdf_file, 'rb') as f:
                    reader = PdfReader(f)
                    for page_num, page in enumerate(reader.pages):
                        text = page.extract_text()
                        self.documents.append({
                            'file': pdf_file.name,
                            'page': page_num,
                            'content': text
                        })
            except Exception as e:
                print(f"Error loading {pdf_file}: {e}")
        
        if self.documents:
            contents = [doc['content'] for doc in self.documents]
            self.tfidf_matrix = self.vectorizer.fit_transform(contents)
    
    def retrieve(self, query: str, top_k: int = 3) -> list:
        """Retrieve top-k relevant documents."""
        if self.tfidf_matrix is None:
            return []
        
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix)[0]
        top_indices = np.argsort(similarities)[-top_k:][::-1]
        
        results = [
            {
                'document': self.documents[i],
                'score': similarities[i]
            }
            for i in top_indices if similarities[i] > 0
        ]
        return results
    def add_pdf(self, pdf_path: str):
        """Add a new PDF and update the TF-IDF matrix."""
        try:
            with open(pdf_path, 'rb') as f:
                reader = PdfReader(f)
                for page_num, page in enumerate(reader.pages):
                    text = page.extract_text()
                    self.documents.append({
                        'file': os.path.basename(pdf_path),
                        'page': page_num,
                        'content': text
                    })
            # Update TF-IDF matrix
            contents = [doc['content'] for doc in self.documents]
            self.tfidf_matrix = self.vectorizer.fit_transform(contents)
        except Exception as e:
            print(f"Error adding {pdf_path}: {e}") 
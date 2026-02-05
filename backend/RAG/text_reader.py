from pathlib import Path
from PyPDF2 import PdfReader
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)



def read_pdf(file_path: str) -> list[str]:
    """Read a PDF file and return a list of text chunks."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    splits = text_splitter.split_text(text)
    return splits

def read_json(file_path: str) -> list[str]:
    """Read a JSON file and return a list of text chunks."""
    with open(file_path, "r") as f:
        data = json.load(f)
    text = json.dumps(data)
    splits = text_splitter.split_text(text)
    return splits

def read_others(file_path: str) -> list[str]:
    """Read other file types and return a list of text chunks."""
    with open(file_path, "r") as f:
        text = f.read()
    splits = text_splitter.split_text(text)
    return splits

def load_and_split(file_path:Path|str) -> list[str]:
    """Load a file and split it into text chunks."""
    if str(file_path).endswith(".pdf"):
        return read_pdf(file_path)
    elif str(file_path).endswith(".json"):
        return read_json(file_path)
    else:
        return read_others(file_path)
    
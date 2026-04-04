from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama
from .rag import PDFRetriever
import ollama



def get_all_ollama_models():
    try:
        models = ollama.list().models
        return [model.model for model in models]
    except Exception as e:
        print(f"Error fetching Ollama models: {e}")
        return []


class Agent:
    def __init__(self,retriever: PDFRetriever,ollama_model: str = "qwen3:1.7b"):
        self.retriever = retriever
        model = ChatOllama(model=ollama_model)
        prompt_template = PromptTemplate.from_template(
            "You are a helpful assistant. Use the following retrieved information to answer the question.\n\n"
            "Retrieved Information:\n{retrieved_info}\n\n"
            "Question: {question}\n\n"
            "Answer:"
        )
        self.chain = prompt_template | model
    
    def answer_question(self, question: str) -> str:
        retrieved_docs = self.retriever.retrieve(question)
        retrieved_info = "\n".join(
            f"{doc['document']['file']} (Page {doc['document']['page']}): {doc['document']['content']}"
            for doc in retrieved_docs
        )
        response = self.chain.invoke({
            "retrieved_info": retrieved_info,
            "question": question,
        })
        return response.content
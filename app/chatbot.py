# app/chatbot.py

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema.runnable import RunnableConfig
from langchain_core.documents import Document
from vector_store import load_vector_store
from config import OPENAI_API_KEY

# Customize prompt to cite sources
QA_TEMPLATE = """You are a helpful assistant for answering customer support questions.

Use the following context to answer the question. If the answer cannot be found, say "I couldn't find an answer in the provided documents."

Always cite the source as (Source: filename, page X) at the end of the sentence.

Context:
{context}

Question: {question}
Answer:"""

qa_prompt = PromptTemplate(
    template=QA_TEMPLATE,
    input_variables=["context", "question"]
)

def initialize_qa_chain():
    vectorstore = load_vector_store()
    retriever = vectorstore.as_retriever(search_type="similarity", k=4)

    llm = ChatOpenAI(temperature=0, openai_api_key=OPENAI_API_KEY)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": qa_prompt},
        return_source_documents=True
    )
    return qa_chain


def answer_query(question: str) -> dict:
    # Handle greetings
    if question.lower().strip() in ["hi", "hello", "hey"]:
        return {
            "response": "👋 Hi there! How can I assist you with your documents today?",
            "offer_ticket": False
        }

    qa_chain = initialize_qa_chain()
    result = qa_chain({"query": question})

    answer = result["result"]
    sources = result.get("source_documents", [])

    fallback_phrases = [
        "I couldn't find an answer",
        "I do not have enough information",
        "I'm not sure",
        "Based on the provided documents, I cannot"
    ]

    low_confidence = any(phrase.lower() in answer.lower() for phrase in fallback_phrases)
    offer_ticket = low_confidence or not answer.strip()

    if offer_ticket:
        answer = "🤔 I couldn’t confidently answer your question based on the provided documents.\nWould you like to create a support ticket for this?"

    if sources:
        answer += "\n\n🔍 I tried looking here:\n"
        for doc in sources:
            meta = doc.metadata
            answer += f"- {meta.get('source')} (page {meta.get('page')})\n"

    return {
        "response": answer,
        "offer_ticket": offer_ticket
    }

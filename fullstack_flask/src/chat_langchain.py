from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain_pinecone import PineconeVectorStore
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import ConversationalRetrievalChain
from pinecone import Pinecone
from .models import db, ChatMessage
import os
from dotenv import load_dotenv

load_dotenv()
# Initialize Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

print("Connecting to Pinecone index")
index_name = 'mental-health-chatbot'
index = pc.Index(index_name)
index.describe_index_stats()

# Initialize VectorStore

text_field = "question"
embeddings = OpenAIEmbeddings(model='text-embedding-ada-002')
vectorstore = PineconeVectorStore(index, embeddings, text_field)

print("Creating chains")
template = """You are a helpful mental health assistant.
Here is a database of mental health questions and answers.

If you find a relevant question, return the answer. Otherwise, say please contact your doctor or IMH Mental Health Helpline at 6389 2222.
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# Initialize LLM and memory
llm = ChatOpenAI(streaming=True)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create retriever and retrieval chain
retriever = vectorstore.as_retriever()

retrieval_chain = (
    {
        "context": retriever.with_config(run_name="Docs"),
        "question": RunnablePassthrough(),
    }
    | prompt
    | llm
    | StrOutputParser()
)

def call_chat(question):
    answer = ""
    try:
        # Stream the response from the retrieval chain
        for chunk in retrieval_chain.stream(question):
            answer += chunk
            yield {"token": chunk}

        # Save the chat message to the database
        chat_message = ChatMessage(user_id=1, question=question, answer=answer)
        db.session.add(chat_message)
        db.session.commit()
    except Exception as e:
        # Handle errors (e.g., log the error, rollback the transaction)
        db.session.rollback()
        print(f"Error: {e}")
        yield {"error": str(e)}
    finally:
        # Ensure the session is closed
        db.session.close()

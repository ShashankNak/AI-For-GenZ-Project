from langchain_groq import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

llm = ChatGroq(model="mixtral-8x7b-32768")

embeddings = HuggingFaceEmbeddings()

loader = PyPDFLoader("savedDocs/2311.02480v1.pdf")


docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
)

splits = text_splitter.split_documents(docs)

vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
retriever = vectorstore.as_retriever()

prompt = hub.pull("rlm/rag-prompt")

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

if rag_chain is None:
        print("Please load a pdf file first")
else:
    text = rag_chain.invoke("What is Deep Learning?")
    print(text) 
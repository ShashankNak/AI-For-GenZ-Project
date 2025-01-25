from langchain_groq import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.text import TextLoader
from langchain_community.document_loaders.json_loader import JSONLoader
from langchain_community.document_loaders.excel import UnstructuredExcelLoader
from langchain_community.document_loaders.word_document import Docx2txtLoader
from langchain_community.vectorstores import Chroma

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain import hub

from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


# api = ""
class ChatBot:
    def __init__(self) -> None:
        self.rag_chain = None
        self.llm = None
        self.embeddings = None
        self.initialized = False
        self.pdfTrained = False
        self.textTrained = False
        self.docxTrained = False
        self.csvTrained = False
        self.jsonTrained = False
        self.excelTrained = False


    def helper(self,loader):
        print("Loading and Splitting.........................")
        try:
            docs = loader.load()
            print("Loaded and Split2.........................")
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200,length_function=len,is_separator_regex=False,)
            print("Splitting.........................")
            splits = text_splitter.split_documents(docs)
            print("Split2.........................")
            vectorstore = Chroma.from_documents(documents=splits, embedding=self.embeddings)
            print("Vectorizing.........................")
            # Retrieve and generate using the relevant snippets of the blog.
            retriever = vectorstore.as_retriever()
            print("Retrieving.........................")
            prompt = hub.pull("rlm/rag-prompt")

            print("regchaining******************************")
            self.rag_chain = (
                {"context": retriever | self.format_docs, "question": RunnablePassthrough()}
                | prompt
                | self.llm
                | StrOutputParser()
            )

        except Exception as e:
            print(e)
            return
        
    def initializeKey(self,API_KEY):
        try:
            if self.initialized:
                return
            
            self.llm = ChatGroq(model="mixtral-8x7b-32768",api_key=API_KEY)
            self.embeddings = HuggingFaceEmbeddings()
            
            self.initialized = True
            return
        except Exception as e:
            return
        

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    def chat_with_docs(self, text):
        if self.rag_chain is None:
            return "Please load a pdf file first"
        text = self.rag_chain.invoke(text)
        return text
    

    #for pdf data
    def pdf_data(self, file):
        try:
            if self.pdfTrained:
                print("Already Trained")
                return
            
            loader = PyPDFLoader(f'savedDocs/{file.name}')
            print("Loading PDF.........................")
            self.helper(loader)
            print("PDF Loaded.........................")
            self.pdfTrained = True
            return
        except Exception as e:
            print(e)
            return
    
    
    def docx_data(self, file):
        try:
            if self.docxTrained:
                return
            
            loader = Docx2txtLoader(f'savedDocs/{file.name}') 
            self.helper(loader)
            self.docxTrained = True
            return
        except Exception as e:
            print(e)
            return
        
    def txt_data(self, file):
        try:
            if self.textTrained:
                return
            
            loader = TextLoader(f'savedDocs/{file.name}') 
            self.helper(loader)
            self.textTrained = True
            return
        except Exception as e:
            print(e)
            return
    
    def csv_data(self, file):
        try:
            if self.csvTrained:
                return
            
            loader = CSVLoader(f'savedDocs/{file.name}') 
            self.helper(loader)
            self.csvTrained = True
            return
        except Exception as e:
            print(e)
            return
    
    def json_data(self, file):
        try:
            if self.jsonTrained:
                return
            
            loader = JSONLoader(f'savedDocs/{file.name}') 
            self.helper(loader)
            self.jsonTrained = True
            return
        except Exception as e:
            print(e)
            return
    
    def xlsx_data(self, file):
        try:
            if self.excelTrained:
                return
            loader = UnstructuredExcelLoader(f'savedDocs/{file.name}') 
            self.helper(loader)
            self.excelTrained = True
            return
        except Exception as e:
            print(e)
            return
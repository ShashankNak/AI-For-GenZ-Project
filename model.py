from langchain_groq import ChatGroq
from langchain import hub
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader, CSVLoader, JSONLoader, UnstructuredExcelLoader
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings


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
        docs = loader.load_and_split()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        splits = text_splitter.split_documents(docs)
        vectorstore = Chroma.from_documents(documents=splits, embedding=self.embeddings)
        # Retrieve and generate using the relevant snippets of the blog.
        retriever = vectorstore.as_retriever()
        prompt = hub.pull("rlm/rag-prompt")

        self.rag_chain = (
            {"context": retriever | self.format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def initializeKey(self,API_KEY):
        try:
            if self.initialized:
                return
            self.llm = ChatGroq(temperature=0, model_name="mixtral-8x7b-32768",api_key=API_KEY)
            self.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
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
                return
            
            loader = PyPDFLoader(f'savedDocs/{file.name}')
            
            self.helper(loader)
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
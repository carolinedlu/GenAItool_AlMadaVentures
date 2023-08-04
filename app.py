from langchain.chains import ConversationalRetrievalChain
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
import streamlit as st 
#HuggingFaceEmbeddings
from langchain.vectorstores import FAISS 
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI 
from langchain.chains import ConversationalRetrievalChain
#from docx import Document
from docx2txt import process
import dropbox
from htmlTemplates import css,bot_template,user_template
from config import OPEN_API_KEY

# def connect_to_dropbox(access_token):
#     try:
#         dbx = dropbox.Dropbox(access_token)
#         return dbx
#     except dropbox.exceptions.AuthError as e:
#         print("Error connecting to Dropbox:", e)
#         return None
    
def get_pdf_text(pdf_docs):
    text = ""
    #loop through the pdfs docs 
    for pdf in pdf_docs: 
        pdf = PdfReader(pdf)
        for page in pdf.pages: 
            text += page.extract_text()
    return text 

def get_word_text(word_docs):
    text = ""
    for doc in word_docs:
        document = process(doc)
        for paragraph in document.paragraphs:
            text += paragraph.text
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator = '\n',
        chunk_size = 1000,
        chunk_overlap = 100, 
        length_function = len 
        )
    chunks = text_splitter.split_text(text)
    #return list of chunks 
    return chunks 

def get_vectorstore(text_chunks):
    embeddings = OpenAIEmbeddings(openai_api_key=OPEN_API_KEY)
    #embeddings = HunggingFaceInstructEmbeddings(model_name = 'hkunlp/instructor-xl')
    vectorstore = FAISS.from_texts(texts = text_chunks,embedding = embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    llm = ChatOpenAI(openai_api_key=OPEN_API_KEY)
    memory = ConversationBufferMemory(memory_key='chat_history',return_messages = True )
    conversation_chain =  ConversationalRetrievalChain.from_llm(
        llm = llm, 
        retriever =  vectorstore.as_retriever(),
        memory = memory
        )
    return conversation_chain 

def handle_userinput(user_question): 

    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message.content), unsafe_allow_html=True)


def main(): 
    load_dotenv()
    #st.session_state.conversation = None
    #st.session_state.conversation = None
    st.set_page_config(page_title='Chat with multiple Al Mada VC documents',page_icon=":books:")

    #adding the css 
    st.write(css,unsafe_allow_html=True)

    #initalization of the session state 
    if "conversation" not in st.session_state:
         st.session_state.conversation =  None
    
    if "chat_history" not in st.session_state : 
         st.session_state.chat_history = None 

    st.header("Chat with multiple Al Mada VC documents :books: ")
    user_question = st.text_input("Ask a question about your documents:")
    

    if user_question: 
            handle_userinput(user_question)


    with st.sidebar: 
        st.subheader("Your documents")
        documents = st.file_uploader("Upload your documents here and press Process", accept_multiple_files=True,
                                     type=["pdf", "docx"])

        if st.button('Process'):
            with st.spinner("Processing"):
                raw_text = ""

                for document in documents:
                    if document.type == "application/pdf":
                        raw_text += get_pdf_text([document])
                    elif document.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        raw_text += get_word_text([document])

            #get the text chunks 
                text_chunks = get_text_chunks(raw_text)

            #create vector stores (can be done using Open AI API or other embeding models (but needs GPU))
                vector_store = get_vectorstore(text_chunks)
            
            #create conversation chain (persistant- variable is linked to the session state)- the variable wont be reinitalized 
            #available outside of the scope 
                st.session_state.conversation = get_conversation_chain(vector_store)

    


if __name__ == '__main__': 
    main()
import openai
import os
import base64
import pandas as pd
from dotenv import load_dotenv
import faiss
import numpy as np
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

load_dotenv()

class RAG:
    def __init__(self, df, text_column='name'):
        self.df = df
        self.text_column = text_column
        self.embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
        self.index = None
        self.vectorstore = None
        self.initialize_db_based_on_df()

    # def load_data(self):    
    #     texts = self.df[self.text_column].tolist()
    #     self.categories = self.df['category'].tolist()
    #     self.index = FAISS.from_texts(texts, self.embeddings)

    def find_similar_category(self, query, k=3):
        results = self.vectorstore.similarity_search_with_score(query=query, k=k)
        return results

    def initialize_db_based_on_df(self):
        df_loader = DataFrameLoader(self.df, page_content_column=self.text_column)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=25000, chunk_overlap=10)
        texts = text_splitter.split_documents(df_loader.load())
        self.vectorstore = FAISS.from_documents(texts, self.embeddings)

if __name__ == "__main__":
    # Example DataFrame
    df = pd.read_csv('data.csv')

    # Initialize RAG model with dataframe
    rag = RAG(df=df, text_column='description')
    
    text = '''
    In the image, there is a jar of pickles placed on a wooden surface. 
    The jar is sealed with a metal lid and contains whole cucumbers, 
    garlic cloves, dill, and what appears to be pickle brine.
    '''
    most_similar_category = rag.find_similar_category(text)
    print("Most similar category:", most_similar_category)

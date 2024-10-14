
import os
import requests

import pypdfium2 # Needs to be at the top to avoid warnings
import argparse
import json
import textwrap
import torch

import numpy as np 
import pandas as pd
from tqdm.auto import tqdm 
from nltk import sent_tokenize

from marker.convert import convert_single_pdf
from marker.logger import configure_logging
from marker.models import load_all_models
from marker.output import save_markdown

from sentence_transformers import util, SentenceTransformer

# For instance of Qdriant data base.
from qdrant_client.models import PointStruct
from qdrant_client.models import Distance, VectorParams

# from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient

from langchain_community.chat_models import ChatOllama

from Tundah.Classes.utility import Utility
from Tundah.Classes.pdf import Pdf
from Tundah.Classes.videoYoutube import VideoYoutube
from Tundah.Classes.data_source import Datasource
from Tundah.Classes.storage import Storage
from Tundah.Classes.shunkHandler import ShunkHandler
from Tundah.Classes.model import Model
from Tundah.Classes.markerModel import MarkerModel
from Tundah.Classes.llmModel import LLMModel
from Tundah.Classes.embeddingModel import EmbeddingModel

 
# Get Documents objects
pdf_objects = Pdf()
youtube_video = VideoYoutube()
embeddingModding = EmbeddingModel()
markerModel = MarkerModel()
llm = LLMModel()
storage = Storage()

json_video_path = "./Transcript_path/Videos.json"


def main():
    # Global Utility
    main_utility = Utility()
    
    # Define device
    device = Utility.get_device()
    
    # Differents populars languages used in Africa
    languages_targets = main_utility.languages
    
    # Embedding models
    model_lst = markerModel.model_lst
    
    # Get PDFs files paths
    # files_path = pdf_objects.get_file_path()
    # print(files_path)
    # print(os.getcwd())
     
    # Ensure output directory exists
    # main_utility.create_dir(pdf_objects.output_dir)
    
    chunks_final_state = pdf_objects.pdf_shunk_list()
    
    vectors = embeddingModding.create_embeddings(chunks_final_state)
    

    # videos_shunk_list = youtube_video.transcriptions_shunk_list()
    
    # videos_vectors = embeddingModding.create_embeddings(videos_shunk_list)
    
    # Insertion in Qdrant database.
    # storage.insert_to_qdriant(videos_vectors, videos_shunk_list)
    storage.insert_to_qdriant(vectors, chunks_final_state)
    
    # query = "What are the traditional steps involved in a Luo customary marriage?" 
    # query = "What are the traditional steps involved in Zimbabwe customary marriage?"
    query = "What is the role of the family in traditional marriage in Wassoulou?"
    # query = "How has the perception of marriage evolved in Wassoulou?" 
    query_embeded = embeddingModding.create_query_embeddings(query)
    
    # Get Context
    context = storage.search_documents(query_embeded)
    # context_texts = pdf_objects.get_context(context)
    
    # Infer From the context
    llm.infer(query, context)
    
    # Processing Video of youtube as data
    # videos_shunk_list = youtube_video.transcriptions_shunk_list()
    
    # videos_vectors = embeddingModding.create_embeddings(videos_shunk_list)
    # storage.insert_to_qdriant(videos_vectors, videos_shunk_list) 
    
if __name__ == '__main__':
    main()













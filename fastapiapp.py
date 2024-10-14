from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
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

app = FastAPI()

# Initialize necessary components
pdf_objects = Pdf()
youtube_video = VideoYoutube()
embeddingModding = EmbeddingModel()
markerModel = MarkerModel()
llm = LLMModel()
storage = Storage()

# class QueryModel(BaseModel):
#     query: str

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
@app.get("/")
def get_landing(): 
    return "Hello word"

@app.post("/ask")
async def ask_question(query: str):
    try:
        # Extract query from the request body
        user_query = query
        print("Backend Query :", user_query)
        # Create embeddings for the user query
        query_embeded = embeddingModding.create_query_embeddings(user_query)
        
        # Search documents for the given query embedding
        context = storage.search_documents(query_embeded)
        
        # If no context is found, raise an exception
        if not context:
            raise HTTPException(status_code=404, detail="Context not found for the given query")
        
        # Perform inference with the LLM and context
        response = llm.infer(user_query, context)
        
        # Return the response to the user
        return {"query": user_query, "response": response}
    
    except Exception as e:
        # Handle any errors that occur during processing
        raise HTTPException(status_code=500, detail=str(e))
    
    
@app.post("/context")
async def get_context(query: str):
    try:
        # Extract query from the request body
        user_query = query
        print("Backend Query :", user_query)
        # Create embeddings for the user query
        query_embeded = embeddingModding.create_query_embeddings(user_query)
        
        # Search documents for the given query embedding
        context = storage.search_documents(query_embeded)
        
        # If no context is found, raise an exception
        if not context:
            raise HTTPException(status_code=404, detail="Context not found for the given query")
        
        return { "response": context}
    
    except Exception as e:
        # Handle any errors that occur during processing
        raise HTTPException(status_code=500, detail=str(e))

# Start FastAPI using the command below (if running as script)
# uvicorn <script_name>:app --reload


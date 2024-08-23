import numpy as np

import streamlit as st
import streamlit.components.v1 as components

from datetime import datetime


# ___________________________________________

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

# ___________________________________________
 
# Get Documents objects
pdf_objects = Pdf()
youtube_video = VideoYoutube()
embeddingModding = EmbeddingModel()
markerModel = MarkerModel()
llm = LLMModel()
storage = Storage()

# Global Utility
main_utility = Utility()

# Define device
device = Utility.get_device()

# Differents populars languages used in Africa
# languages_targets = main_utility.languages

# Embedding models
# model_lst = markerModel.model_lst

# Get PDFs files paths
# files_path = pdf_objects.get_file_path()
# print(files_path)
# print(os.getcwd())
    
# Ensure output directory exists
# main_utility.create_dir(pdf_objects.output_dir)

# ___________________________________________

# Set up page configuration
st.set_page_config(page_title="Chat Interface", page_icon=":speech_balloon:", layout="wide")

# Define the columns
left_col, main_col, right_col = st.columns([2, 5, 2])

chat_list =  ["Tundah", "Mariage", "PolyGami", "Divoce", "Childreen", "Tradition"]

# Left column - List of chats
with left_col:
    st.write("")  # To create some space at the top
    st.markdown('<div class="fixed-column">', unsafe_allow_html=True)
    for user in chat_list:
        st.markdown(
            f"""
            <div style="border-bottom: 1px solid #ddd; padding: 10px 0;">
                <img src="https://via.placeholder.com/50" style="border-radius: 50%; vertical-align: middle; margin-right: 10px;">
                <strong>{user}</strong><br>
            </div>
            """, unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)


# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        ("assistant", "Cool, don't forget to bring your ice skates unless you want to use theirs."),
        ("user", "I wish! Don't have those bad boys anymore, will use theirs."),
        ("assistant", "It's all good. It will come back quick. 😊"),
        ("user", "Wow! Where did you snap that? Looks really nice."),        
        
        ("user", "Wow! Another Test")
    ]
    
    # Store and clear the input value in the session state
    if "new_message" not in st.session_state:
        st.session_state.new_message = ""
    
      
# Main column - Chat area
with main_col:
    # st.write("")  # To create some space at the top
    st.markdown('<div class="main-column">', unsafe_allow_html=True)
    
    for role, message in st.session_state.messages:
        align = "right" if role=='user' else "left"
        color = "#7873a5" if role=='user' else "#e9ebf2"
        
        if role == 'assistant':
            message_html = f"""
            <div style="display: flex; justify-content: {align}; align-items: end; margin-bottom: 10px; position: relative; background-color: #2f2f2f; ">
                <img src="https://via.placeholder.com/40" style="border-radius: 50%; vertical-align: bottom; margin-right: 10px;">
                <div style="background-color: {color}; padding: 10px 20px; border-radius: 20px; border-botom-left-radius: 0px; color: black; max-width: 70%;">
                    {message}
                </div>
            </div>
            """
        else:
            message_html = f"""
            <div style="display: flex; justify-content: {align}; align-items: end; margin-bottom: 10px; position: relative; background-color: #2f2f2f;">
                <div style="background-color: {color}; padding: 10px 20px; border-radius: 20px; color: white; max-width: 70%;">
                    {message}
                </div>
                <img src="https://via.placeholder.com/40" style="border-radius: 50%; vertical-align: bottom; margin-left: 10px;">
            </div>
            """
        st.markdown(message_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
        
    # Text input at the bottom with form
    with st.form("message_form", clear_on_submit=True):
        query = st.text_input("Type your question...", value="", key="new_message", placeholder="Type your question here...")
        submit_button = st.form_submit_button("Send")
    # Text input at the bottom
    # message = st.text_input("Type your question...", value="", key="input_message", placeholder="Type your question here...")

    if submit_button and query :
        st.session_state.messages.append(("user", query))
        query_embeded = embeddingModding.create_query_embeddings(query)
        context = storage.search_documents(query_embeded)
        response = llm.infer(query, context)
        st.session_state.messages.append(("assistant", response))
        st.session_state.input_message = ""
    # st.experimental_rerun()
        
        
# Right column - User profile
with right_col:
    st.write("")  # To create some space at the top
    st.markdown('<div class="fixed-column">', unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center; color: white;">
            <img src="https://via.placeholder.com/100" style="border-radius: 50%;">
            <h2>Jess Albertson</h2>
            <p>Perth, Australia</p>
            <p>I believe in labors of love. Mine are surfing and long walks on the beach with my husband and dog. I also love writing and poetry.</p>
            <button style="background-color: #6cd625; border: none; color: white; padding: 10px 20px; border-radius: 20px; cursor: pointer;">
                Email me
            </button>
        </div>
        """, unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
# Define custom CSS styles
st.markdown("""
    <style>
        body {
            background-color: white;
        }
        .main-column {
            background-color: #2f2f2f;
            padding: 20px;
            overflow-y: auto;
            height: 100%;
            border-left: 1px solid white;
            border-right: 1px solid white;
            position: relative;
        }
        .fixed-column {
            position: sticky;
            top: 0;
            background-color: black;
            
        }
    </style>
""", unsafe_allow_html=True)






# Set page title and favicon
# st.set_page_config(page_title="Simple Chat App", page_icon=":speech_balloon:", layout="wide")

# # Layout with three columns: left, main, right
# left_col, main_col, right_col = st.columns([2, 5, 2])

# # Left Sidebar (Mimicked with a column)
# with left_col:
#     st.markdown("### Chats")
#     chat_list = ["Chat 1", "Chat 2", "Chat 3", "Create New Chat"]
#     selected_chat = st.selectbox("Select or create a chat", chat_list)

# # Right Sidebar (Mimicked with a column)
# with right_col:
#     st.markdown("### Profile")
#     st.image("https://via.placeholder.com/150", width=150, caption="Profile Picture", use_column_width=True)
#     st.markdown("""
#         #### **Name:** 
#         John Doe  
#         #### **Bio:** 
#         A passionate tech enthusiast and software developer.
#     """)

# # Main content (Chat window)
# with main_col:
#     # Add custom CSS for styling
#     st.markdown("""
#         <style>
#         .chat-container {
#             width: 100%;
#             padding: 10px;
#             background-color: #f1f1f1;
#             height: 100vh;
#             overflow-y: auto;
#             position: absolute;
#         }
#         .chat-message {
#             padding: 10px;
#             margin: 5px;
#             border-radius: 5px;
#             background-color: #e0e0e0;
#             position: relative;
#         }
#         .chat-message.user {
#             background-color: #7873a5;
#             text-align: right;
#         }
#         .chat-message.bot {
#             background-color: #e9ebf2;
#             color: #000;
#         }
#         .timestamp {
#             font-size: 0.7em;
#             color: #888;
#         }
#         .timestamp.user {
#             color: #FFF;
#         }
#         .input-container {
#             width: 80%;
#             position: fixed;
#             bottom: 0;
#             left: 10%;
#             padding: 10px;
#             background-color: #FFFS;
#             color: #000;
#         }
#         .stTextInput>div>div>input {
#             width: 100%;
#             padding: 10px 40px 10px 20px;
#             border-radius: 20px;
#             border: 1px solid #6fd131;
#             font-family: 'Arial', sans-serif;
#             font-size: 16px;
#             background-color: #f9f9f9;
#             color: #000;
#         }
#         .stTextInput>div>div {
#             position: relative;
#         }
#         .stTextInput>div>div::after {
#             content: '✉️';
#             position: absolute;
#             right: 15px;
#             top: 50%;
#             transform: translateY(-50%);
#             font-size: 18px;
            
#         }
#         </style>

#     """, unsafe_allow_html=True)

#     # Initialize session state for chat history
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     # Function to display chat messages
#     def display_chat():
#         st.markdown('<div class="chat-container">', unsafe_allow_html=True)
#         for message in st.session_state.messages:
#             user_class = "user" if message["user"] == "You" else "bot"
#             st.markdown(
#                 f'<div class="chat-message {user_class}">'
#                 f'{message["text"]}<div class="timestamp {user_class}">{message["time"]}</div></div>',
#                 unsafe_allow_html=True,
#             )
#         st.markdown('</div>', unsafe_allow_html=True)
        

#     # Display chat history
#     display_chat()

#     # Store and clear the input value in the session state
#     if "new_message" not in st.session_state:
#         st.session_state.new_message = ""

#     # Input for new message, styled with envelope icon
#     with st.container():
#         st.markdown('<div class="input-container">', unsafe_allow_html=True)
#         new_message = st.text_input("You: ", value="", label_visibility="hidden")
#         st.markdown('</div>', unsafe_allow_html=True)

#     # When the user sends a message
#     if new_message :
#         current_time = datetime.now().strftime('%H:%M')

#         # Add the user's message to the chat history
#         st.session_state.messages.append({"user": "You", "text": new_message, "time": current_time})

#         # Add a bot response (a simple echo in this case)
#         st.session_state.messages.append({"user": "Bot", "text": f"Echo: {new_message}", "time": current_time})

#         # Refresh the chat display
#         display_chat()

#         # Clear the input field manually by resetting it
#         st.experimental_rerun()
        






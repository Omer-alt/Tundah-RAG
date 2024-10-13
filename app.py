import streamlit as st
from PIL import Image

from Tundah.Classes.embeddingModel import EmbeddingModel
from Tundah.Classes.llmModel import LLMModel
from Tundah.Classes.storage import Storage
from Tundah.Classes.utility import Utility

# Load image from local directory
image = Image.open('static/ai_icon.png')

# Initialize objects
embeddingModding = EmbeddingModel()
llm = LLMModel()
storage = Storage()

# Global Utility
main_utility = Utility()

# Define device
device = Utility.get_device()

# Set up page configuration
st.set_page_config(page_title="Chat Interface", page_icon=":speech_balloon:", layout="wide")

# Define the columns
left_col, main_col, right_col = st.columns([2, 5, 2])

# Sample chat list
chat_list = ["Tundah", "Mariage", "PolyGamy", "Divorce", "Children", "Tradition"]

def handle_submit():
    # Add user's message to session state
    st.session_state.messages.append(("user", st.session_state.new_message))
    

# Left column - List of chats
with left_col:
    st.markdown('<div class="fixed-column-left">', unsafe_allow_html=True)
    for user in chat_list:
        st.markdown(
            f"""
            <div style="border-bottom: 1px solid #ddd; padding: 10px 0;">
                <img src="https://via.placeholder.com/50" style="border-radius: 50%; vertical-align: middle; margin-right: 10px;">
                <strong style="cursor: pointer;">{user}</strong><br>
            </div>
            """, unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        ("assistant", "Welcome to Tündah, your essential guide to African wedding traditions. I'm your AI assistant, steeped in cultural knowledge. How can I help you explore these rich traditions today?"),

    ]

# Main column - Chat area with vertical borders
with main_col:
    st.markdown(
    """
    <div  style="position: absolute; display: flex; justify-content: space-between; align-items: start; width: 100%; height: 100vh; border-left: 2px solid #ddd; overflow: hidden;">
        <!-- Main content -->
        <div style="flex: 1; margin:60px; position: relative; padding-left: 40px; padding-right: 40px; width: 95% ">
            
    """, unsafe_allow_html=True)

    for role, message in st.session_state.messages:
        align = "right" if role == 'user' else "left"
        color = "#7873a5" if role == 'user' else "#e9ebf2"

        if role == 'assistant':
            message_html = f"""
            <div style="display: flex; justify-content: {align}; align-items: end; margin-bottom: 10px; margin-left: 20px; ">
                <img src="https://via.placeholder.com/40" style="border-radius: 50%; vertical-align: bottom; margin-right: 10px;">
                <div style="background-color: {color}; padding: 10px 20px; border-radius: 20px; border-bottom-left-radius: 0px; color: black; max-width: 70%;">
                    {message}
                </div>
            </div>
            """
        else:
            message_html = f"""
            <div style="display: flex; justify-content: {align}; align-items: end; margin-bottom: 10px; ">
                <div style="background-color: {color}; padding: 10px 20px; border-radius: 20px; border-bottom-right-radius: 0px; color: white; max-width: 70%;">
                    {message}
                </div>
                <img src="https://via.placeholder.com/40" style="border-radius: 50%; vertical-align: bottom; margin-left: 10px;">
            </div>
            """
        st.markdown(message_html, unsafe_allow_html=True)

    st.markdown(
    """
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Text input at the bottom with form
    with st.form("message_form", clear_on_submit=True):
        query = st.text_input("Type your question...", value="", key="new_message", placeholder="Type your question here...")
        submit_button = st.form_submit_button("Send", on_click=handle_submit)
    # Text input at the bottom
    # message = st.text_input("Type your question...", value="", key="input_message", placeholder="Type your question here...")

    if submit_button and query :
        # st.session_state.messages.append(("user", query))
   
        query_embeded = embeddingModding.create_query_embeddings(st.session_state.new_message)
        context = storage.search_documents(query_embeded)
        
        # Insert a placeholder for the assistant's response
        response_placeholder = st.empty()
        
        response = llm.infer(st.session_state.new_message, context)
        st.session_state.messages.append(("assistant", response))
        st.session_state.input_message = ""
        
        # After updating session state, optionally force a rerun to immediately reflect changes
        st.rerun()
        
    st.markdown(
    """
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Right column - User profile with violet background 
with right_col:
    st.markdown('<div class="fixed-column-right">', unsafe_allow_html=True)
    # Display image
    # st.image(image, use_column_width=False)

    # Afficher l'image  
    # st.image(image, use_column_width=False)
    st.markdown(
        """
        <div style="background-color: #7873a5; text-align: center; color: white; margin-left: 40px; width: 100%; position: absolute; top: 50px;">
            <img src="https://via.placeholder.com/100" style="border-radius: 50%;">
            <h2 style="color: white;">Tündah</h2>
            <p >African Heritage</p>
            <p style="font-size: 18px; text-align: justify;" >
                Tündah is a web platform dedicated to showcasing how weddings are traditionally organized in Africa. Created as an academic project, Tündah was developed by five software engineering students who are passionate about African culture. They recognized the threat of misinformation surrounding customary marriages and decided to use their skills in software development to create this platform. 
            </p>
            <p style="font-size: 18px; text-align: justify;">
                This project aims to combat misinformation by providing accurate and detailed information about African wedding traditions. While the focus starts with Cameroon, Kenya and Senegal the team envisions expanding Tündah to cover a broader range of African cultures in the future. Tündah a commitment to preserving African heritage and promoting cultural awareness through technology.
            </p>
            <a href="https://github.com/dilane3/tundah-app" target="_blank" style="display: inline-block; background-color: #6cd625; border: none; color: white; padding: 10px 20px; border-radius: 20px; cursor: pointer; text-decoration: none; text-align: center; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); transition: box-shadow 0.3s ease;">
                See Tündah
            </a>
        </div>
        """, unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

# Define custom CSS styles
st.markdown("""
    <style>
        body {
            background-color: black;
        }
        .fixed-column-left {
            position: fixed;
            height: 100vh;
            background-color: #7873a5;
            margin: 10px 0;
        }
        .fixed-column-right {
            display: flex;
            align-content: start;
            position: fixed;
            height: 100vh;
            width: 123%;
            background-color: #7873a5;
        }
    </style>
""", unsafe_allow_html=True)

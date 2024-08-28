# Advenced RAG 

Local RAG pipeline we're going to build:

!["This is a flowchart describing a local retrieval-augmented generation (RAG) workflow for document, youtube videos processing and embedding creation, followed by search and answer functionality. The process begins with a collection of documents, such as PDFs, Youtube link (a Json file with youtube videos link), which are preprocessed into smaller chunks, (for example group of 384 characters). These chunks are used as context for the Large Language Model (LLM). A cool person (potentially the user) asks a query such as "WWhat is the role of the family in traditional marriage in Wassoulou?" This query is then transformed by an embedding model into a numerical representation using sentence transformers, which are stored in a Qdrant vector database, suitable for extremely large datasets. The numerical query and relevant document passages are processed on a local GPU, MPS OR CPU, According to your material. The LLM generates output based on the context related to the query, which can be interacted with through an optional chat web app interface made with streamlit.Let see the flowchart."](images/simple-local-rag-workflow-flowchart.png)

All using open-source tools.

In our specific example, we will create TündahChat, a RAG workflow that allows a person to query knowledge bases about customary marriage practices in Africa in general.

Note: [Tündah](https://github.com/dilane3/tundah-app) is a web platform where information is published on how marriages are organized in Cameroon in particular and in Africa in general.
 

You can also run notebook `Tundah.ipynb` directly in locally

### Project Structure 

- `Tundah.ipynb`: This notebook outlines the sequential workflow of Tundah-RAG, providing a step-by-step process.
- `assets`: A repository for supplementary data that supports the project.

- `Pdf_path`:This directory holds all the source PDFs, which serve as the information backbone for our RAG system.
- `static`: Contains supplementary assets related to the Streamlit interface, including logos and other media.
- `Structured_file`:Stores the processed results of the PDFs, refined through the Marker model for structured output.
- `Transcript_path`:Includes the video.json file, which contains links and titles of YouTube videos relevant to customary marriages in Africa.
- `Tundah/Classes`: This folder organizes classes designed to structure our codebase, making it reusable, maintainable, and compliant with best practices in software engineering.

- `main.py`: Provides a command-line interface for testing the code.
- `streamlit.py`:The Streamlit interface facilitates a seamless user-RAG interaction, enhancing usability.

## Dataset 
The dataset used to build the RAG system focuses on aspects related to customary marriages in 10 African countries: Cameroon, Kenya, Nigeria, South Africa, Zimbabwe, Tanzania, Uganda, Botswana, and Mali. Currently, the data is sourced from two main channels: cultural articles/books and YouTube videos. In the future, we plan to perform web scraping on websites and blogs that are rich in reliable and accessible information.

## Architecture 

#### Global architecture
![Global architecture](/static/RAG_Architecture.png)
#### UML: Class Diagram
![Class Diagram](/static/RAG_Class_Diagram.png)


## Setup

#### clone
```
git clone https://github.com/Omer-alt/Tundah-RAG.git
```

```
cd Tundah-RAG
```
#### Install requirements

```
pip install -r requirements.txt
```

### Launch notebook

VS Code:

```
code .
```

Jupyter Notebook

```
jupyter notebook
```

#### Run

Lunch docker, run   Qdrant, run ollama
```
open -a docker
docker run -p ['Qdriant_id'] 
ollama run llama2:7b-chat-q4_0

```
Run in the console
```
python main.py
```
Run with streamlit interface
```
streamlit run streamlit.py
```

## Limitations 
-  One significant limitation is the availability of datasets. To address this, I considered using transcripts from YouTube videos. However, another significant challenge arises: the videos deemed relevant by local communities are often in low-resource languages (Example: [Customary marriages in Ghana](https://www.youtube.com/watch?v=5pmEDELq4wA)), which impacts the quality of embeddings and the performance of Large Language Models (LLMs) in such contexts. This issue is highlighted in the recent paper '[IrokoBench: A New Benchmark for African Languages in the Age of Large Language Models](https://arxiv.org/abs/2406.03368)`.

## Perspective
- Creating a Docker Image for the RAG System
- Implementing CI/CD for the RAG System



## Appendix
Tutorials that can help to better understand this project.
- [simple-local-rag](https://github.com/mrdbourke/simple-local-rag)
- [Deep Dive into Retrieval Augmented Generation (RAG) - Architecture & Working of Naive and Advanced RAG Framework.](https://www.linkedin.com/pulse/deep-dive-retrieval-augmented-generation-rag-working-tejas-bankar-q9erf/)
- [Docker Crash Course for Absolute Beginners](https://www.youtube.com/watch?v=pg19Z8LL06w)
- [ChatGPT Prompt Engineering for Developers](https://learn.deeplearning.ai/accomplishments/93a17013-68d7-46ac-a2a5-5a7bf4a8c330)
- [Bases de Données Vectorielles : Expérience & Conseils d'Expert](https://www.youtube.com/watch?v=p427fEARYOs)

## License

[MIT](https://choosealicense.com/licenses/mit/)

------------------------------------------------------------------------------------------------------------

⭐️ If you find this repository helpful, we’d be thrilled if you could give it a star! 






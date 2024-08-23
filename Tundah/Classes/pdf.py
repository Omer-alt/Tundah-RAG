import os

from marker.output import save_markdown

from .data_source import *
from .model import *
from .embeddingModel import *
from .shunkHandler import *

class Pdf(Datasource):
    
    files_path = []
    pdf_vectors = []
    list_paload_pdf = []
    base_json: str
    model: Model
    embeddingModel: EmbeddingModel

    def __init__(self):
        super().__init__()
        self.base_json = "tundah"
        

    def get_file_path(self):
        self.files_path = self.utility.file_pdf_paths(self.docs_path)
        return  self.files_path
    
    def pdf_shunk_list(self):
        
        # Traverse the folder and process each PDF file
        for file in os.listdir(self.docs_path):
            file_path = os.path.join(self.docs_path, file)
            if os.path.isfile(file_path) and file.lower().endswith('.pdf'):
                try:
                    # Perform PDF extraction
                    full_text, images, out_meta = ShunkHandler.convert_single_pdf(file_path)
                    
                    # Split full text into chunks
                    chunks = ShunkHandler.split_into_chunks(full_text, self.max_chunk_size)
                    
                    # Prepare chunks with metadata
                    structured_chunks = []
                    for _, chunk in enumerate(chunks):
                        structured_chunks.append({
                            'page_number': out_meta.get('page_number', 'N/A'),
                            'sentence_chunk': chunk,
                            'chunk_char_count': len(chunk),
                            'chunk_word_count': len(chunk.split()),
                            'chunk_token_count': len(chunk) / self.token_char_ratio
                        })
                    
                    # Check chunk quality
                    filtered_chunks = ShunkHandler.check_chunk_quality(structured_chunks, min_word_count=30, max_token_count=384)
                    self.list_paload_pdf += filtered_chunks
                    # Save extracted content
                    fname = os.path.basename(file_path).replace('.pdf', '')
                    subfolder_path = save_markdown(self.output_dir, fname, full_text, images, out_meta)
                    
                    # Create the JSON output path
                    json_output_path = os.path.join(self.output_dir, f"{self.base_json}_chunks.json")
                    
                    # Append to JSON file
                    self.utility.append_to_json(json_output_path, filtered_chunks)
                    
                    print(f"Saved markdown and JSON to the {subfolder_path} folder")
                    return self.chunks_final_state
                
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

        print("Processing completed.")
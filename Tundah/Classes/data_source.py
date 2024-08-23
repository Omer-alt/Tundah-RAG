from .utility import Utility

class Datasource:
    # Paths
    docs_path = "Pdf_path/"
    output_path = "Structured_files/"
    output_dir = "Structured_files/"
    max_token_limit = 384 
    token_char_ratio = 4
    max_chunk_size = max_token_limit * token_char_ratio

    def __init__(self) -> None:
        self.utility = Utility()
        self.context = []
        
    def get_context(self, context: list) -> list[str]:
        # print(context)
        self.context = [shunk.payload["sentence_chunk"] for shunk in context]
        
        return self.context


            
            
    
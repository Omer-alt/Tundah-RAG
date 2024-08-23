from .model import Model


from marker.convert import convert_single_pdf
from marker.logger import configure_logging
from marker.models import load_all_models
from marker.output import save_markdown

class MarkerModel(Model):

    def __init__(self):
        super().__init__()
        self.model_lst = load_all_models()

    def pdf_extraction(self, file_path):
        
        # Perform PDF extraction
        print(f"Processing file: {file_path}")
        full_text, images, out_meta = convert_single_pdf(file_path, self.model_lst)
        
        return full_text, images, out_meta
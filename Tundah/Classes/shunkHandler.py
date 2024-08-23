import textwrap
from nltk import sent_tokenize

class ShunkHandler:

    @staticmethod
    def recursive_structure_aware_chunking(text, max_chunk_size):
        """
        Splits text based on recursive structure-aware chunking.
        """
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) > max_chunk_size:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += " " + sentence
        
        # Add the last chunk
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks

    @staticmethod
    def sentence_window_parsing(text, window_size=3):
        """
        Splits text into chunks of sentences with overlapping context.
        """
        sentences = sent_tokenize(text)
        chunks = []
        
        for i in range(len(sentences) - window_size + 1):
            chunk = " ".join(sentences[i:i + window_size])
            chunks.append(chunk)
        
        return chunks

    @staticmethod
    def parent_child_chunking(text, max_parent_size, max_child_size):
        """
        Splits text into parent and child chunks.
        """
        # First split into parent chunks
        parent_chunks =ShunkHandler.recursive_structure_aware_chunking(text, max_parent_size)
        child_chunks = []
        
        for parent_chunk in parent_chunks:
            # Further split each parent chunk into child chunks
            children = ShunkHandler.recursive_structure_aware_chunking(parent_chunk, max_child_size)
            child_chunks.extend(children)
        
        return child_chunks

    @staticmethod
    def check_chunk_quality(structured_chunks, min_word_count=30, max_token_count=384):
        """
        Filters out chunks that do not meet the quality criteria.
        """
        filtered_chunks = []

        for chunk in structured_chunks:
            # Check if the chunk meets the quality criteria
            if (chunk['chunk_word_count'] >= min_word_count) and (chunk['chunk_token_count'] <= max_token_count):
                filtered_chunks.append(chunk)

        return filtered_chunks
    
    
    # Method to split text into chunks
    @staticmethod
    def split_into_chunks(text, max_chunk_size):
        return textwrap.wrap(text, max_chunk_size)
    
    
    
    
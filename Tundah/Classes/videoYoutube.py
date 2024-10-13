from youtube_transcript_api import YouTubeTranscriptApi,  NoTranscriptFound
from deep_translator import GoogleTranslator

from .data_source import Datasource
from .shunkHandler import ShunkHandler
from .utility import Utility

class VideoYoutube(Datasource):

    video_id:str
    video_vector = []
    pdf_vectors = []
    list_paload_video = []
    json_video_path = "./Transcript_path/Videos.json"
    
    def __init__(self):
        super().__init__() # Get the contructor of the mother classe


    def get_transcription(self, video_id):
        # max_chars: maximum number of characters that can be translated by google translate
        max_chars = 4998
        target_language = 'en'
        translator = GoogleTranslator(source='auto', target=target_language )

        try:
            # Get the transcript using the YouTubeTranscriptApi
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id, 
                languages=self.utility.languages
            )

            # Combine the transcript text
            transcript_text = " ".join([entry['text'] for entry in transcript])
            
            #  GoogleTranslator has a max size limitation to make text translation.
            if len(transcript_text) >= max_chars:
                #  Split into shunk, translate shunk and join them
                text_shunk = ShunkHandler.split_into_chunks(transcript_text, max_chars) 
                text_shunk_en = [translator.translate(shunk) for shunk in text_shunk]
                transcript_text = " ".join(text_shunk_en)
                
                return transcript_text
            
            # Translate the transcript using GoogleTranslator from deep-translator
            translated_transcript = translator.translate(transcript_text)

            return translated_transcript
        except NoTranscriptFound:
            print(f"No transcript found for video ID: {video_id}")
            return None
        
        
    def transcriptions_shunk_list(self):
        """
        From a JSON file of video, give a list of shunks
        Parameters:
        - json_video_path: Path to the JSON file.

        Returns:
        - transcription_chunks: List of Shunks.
        """
        
        target_language = 'en'
        translator = GoogleTranslator(source='auto', target=target_language)
        
        # Get array of Youtube videos list
        _, data = self.utility.load_json_to_dataframe(self.json_video_path)
        
        # Prepare chunks with metadata
        transcription_chunks = []
        
        # Get the transcript for each videos
        for video in data['videos']:
            
            # Extract the video ID from the URL
            video_url=video['url']
            video_id = video_url.split('v=')[-1]
            
            # Get the full transcript for single video
            translated_text = self.get_transcription(video_id)
            
            if translated_text is None:
                continue  # Skip this video if no transcript is found
            
            print(video['title'], translated_text)
            # Shunk the transtription
            chunks = ShunkHandler.split_into_chunks(translated_text, self.max_token_limit)
                
            for _, chunk in enumerate(chunks):
                transcription_chunks.append({
                    'video_id': video_id,
                    'title': translator.translate(video['title']),
                    'sentence_chunk': chunk,
                    'chunk_char_count': len(chunk),
                    'chunk_word_count': len(chunk.split()),
                    'chunk_token_count': len(chunk) / self.token_char_ratio
                })
            
        
        return transcription_chunks

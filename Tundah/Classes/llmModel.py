from .model import Model

from langchain_community.chat_models import ChatOllama

class LLMModel(Model):
    

    def __init__(self, temperature=0.3):
        super().__init__()
        self.temperature = temperature
        self.local_model = "llama2:7b-chat-q4_0"
        # local_model = "mistral"
        self.llm = ChatOllama(model=self.local_model, temperature=self.temperature)
        
    def get_prompt(self, query: str) -> str:
    # context_str = '\n'.join(context)
    
        return f"""
        SYSTEM: You are an expert on African customary marriage laws. Answer the following questions about marriage practices, annulments, and implications of specific customs across different African tribes.

        Use the following pieces of context to answer the question at the end. Think step-by-step, and then answer. 

        Do not try to make up an answer:
        - If the context can help determine the answer, use it to form your response directly without introductory phrases like "I can determine the answer to that based on the provided context."
        - If the context can help determine the answer, Use the context to craft a well-structured response that aligns with the question asked, integrating relevant information rather than simply copying and pasting excerpts. However, if the context is not useful, say "I cannot determine the answer to that."    - If the context is empty, just say "I do not know the answer to that."
        - If explicitly requested or if you cannot provide a clear answer without explanation, then include the reasoning.

    
        ==================
        Context: {self.source.context}
        ==================

        ### Guidelines:
        1. **Condition Check**: Ensure that each response is accurate, culturally sensitive, and aligns with the specific customary practices of the tribe mentioned.
        2. **Step-by-Step Solution**: Before concluding, think through the cultural, legal, and social aspects of the question, and consider the potential impact on the families and communities involved. 

        Question: {query}
        Helpful Answer:"""

    def infer(self, query, context):
        # Update datasource context.
        self.source.get_context(context)
        
        prompt = self.get_prompt(query=query)

        # Example input in the format expected by the model
        input_data =  [
            {"role": "user", "content": prompt}
        ]

        # Make a prediction
        response = self.llm.invoke(input_data)
        
        print("\n","-"*(4 + len(query) ),"\n")
        print(f"QUERY: {query}")
        print("\n","-"*(4 + len(query)*4 ),"\n")
        print(f"Answer: {response.content}")
        return response.content
        
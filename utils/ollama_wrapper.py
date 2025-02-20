from langchain_core.runnables import Runnable

class OllamaRunnable(Runnable):
    def __init__(self, client):
        self.client = client
    
    def invoke(self, input_data, config=None):
        response = self.client.generate(
            model="deepseek-r1",
            prompt=input_data["input"]
        )
        return response["response"]

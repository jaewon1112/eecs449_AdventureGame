from PIL import Image
import ollama

class ImageProcessor:
    def __init__(self):
        self.client = ollama.Client()
    
    def process_image(self, image_path):
        # 이미지 분석 및 게임 이벤트 생성
        img = Image.open(image_path)
        response = self.client.generate(
            model="llava",
            prompt=f"Describe this image and suggest a story event based on it: {image_path}",
            images=[image_path]
        )
        return response["response"]
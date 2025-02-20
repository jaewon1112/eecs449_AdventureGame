import os
from langchain_core.runnables import Runnable
from langchain.memory import ConversationBufferMemory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain.prompts import PromptTemplate
import ollama
import whisper
from PIL import Image
import pyaudio
import wave
# Optional: Suppress deprecation warning
# import warnings
# warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)

# Custom Runnable for Ollama models
class OllamaRunnable(Runnable):
    def __init__(self, client, model_name):
        self.client = client
        self.model_name = model_name
    
    def invoke(self, input_data, config=None):
        try:
            if isinstance(input_data, dict) and "input" in input_data:
                prompt = input_data["input"]
            elif isinstance(input_data, str) and os.path.exists(input_data):
                prompt = f"Describe this image: {input_data}"
            else:
                prompt = str(input_data)

            print(f"Generating response with {self.model_name} for prompt: {prompt}")
            response = self.client.generate(
                model=self.model_name,
                prompt=prompt
            )
            print(f"Response received: {response['response']}")
            return response["response"]
        except Exception as e:
            print(f"Error in invoke: {str(e)}")
            return f"Error: {str(e)}"

# Game class to manage the adventure
class AdventureGame:
    def __init__(self):
        self.client = ollama.Client()  # Local Ollama client
        self.story_model = OllamaRunnable(self.client, "deepseek-r1")  # Story generation
        self.image_model = OllamaRunnable(self.client, "qwen2:7b-instruct")  # Fallback due to qwen-vl unavailability
        self.whisper_model = whisper.load_model("base")               # Voice transcription
        self.chat_history = InMemoryChatMessageHistory()              # New chat history
        self.memory = ConversationBufferMemory(chat_memory=self.chat_history)  # Updated memory
        self.sidekick_prompt = PromptTemplate(
            input_variables=["history", "input"],
            template="You are a helpful sidekick in an adventure game. Based on the game history: {history}, respond to the player's request: {input}"
        )
        self.story_prompt = PromptTemplate(
            input_variables=["history", "input"],
            template="You are a narrator in a mysterious adventure game set in a strange forest with a bear cub named Cubby. Based on the game history: {history}, continue the story in response to the player's action: {input}. Stay in character, use vivid descriptions, and avoid breaking immersion."
        )

    def start_game(self):
        intro_prompt = "Begin a mysterious adventure story where the player wakes up in a strange forest and encounters a bear cub named Cubby."
        print("Starting game, generating intro...")
        intro = self.story_model.invoke({"input": intro_prompt})
        self.memory.save_context({"input": intro_prompt}, {"output": intro})
        print("=== Adventure Game ===")
        print(intro)
        self.game_loop()

    def process_image(self, image_path):
        if os.path.exists(image_path):
            description = self.image_model.invoke(image_path)
            history = self.memory.load_memory_variables({})["history"]
            story_update = self.story_model.invoke(
                self.story_prompt.format(history=history, input=f"Incorporate this into the story: {description}")
            )
            self.memory.save_context({"input": description}, {"output": story_update})
            print(story_update)
        else:
            print("Image not found!")

    def process_voice(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 44100
        RECORD_SECONDS = 5
        OUTPUT_FILENAME = "input.wav"

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        print("Recording for 5 seconds...")
        frames = []
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("Recording finished.")
        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        result = self.whisper_model.transcribe(OUTPUT_FILENAME)
        text = result["text"]
        return text
 
    def sidekick_advice(self, player_input):
        history = self.memory.load_memory_variables({})["history"]
        sidekick_response = self.story_model.invoke(
            self.sidekick_prompt.format(history=history, input=player_input)
        )
        print(f"Sidekick: {sidekick_response}")

    def game_loop(self):
        while True:
            action = input("\nWhat do you do? (or say 'voice', 'image [path]', 'help', 'exit'): ").strip().lower()
            
            if action == "exit":
                print("Thanks for playing!")
                break
            elif action == "help":
                print("Commands: 'go [direction]', 'use [item]', 'talk to sidekick', 'voice', 'image [path]', 'exit'")
            elif action.startswith("image "):
                image_path = action.split(" ", 1)[1]
                self.process_image(image_path)
            elif action == "voice":
                text = self.process_voice()
                print(f"You said: {text}")
                history = self.memory.load_memory_variables({})["history"]
                response = self.story_model.invoke(
                    self.story_prompt.format(history=history, input=text)
                )
                self.memory.save_context({"input": text}, {"output": response})
                print(response)
            elif "talk to sidekick" in action:
                self.sidekick_advice(action)
            else:
                history = self.memory.load_memory_variables({})["history"]
                response = self.story_model.invoke(
                    self.story_prompt.format(history=history, input=action)
                )
                self.memory.save_context({"input": action}, {"output": response})
                print(response)

if __name__ == "__main__":
    game = AdventureGame()
    game.start_game()
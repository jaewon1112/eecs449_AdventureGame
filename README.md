# Adventure Game
A text-based adventure game using Ollama, LangChain, and Whisper.

## Setup
1. Clone the Repository: https://github.com/jaewon1112/eecs449_AdventureGame.git
2. Install Ollama: https://ollama.ai/
3. Pull models: `ollama pull deepseek-r1`, `ollama pull qwen2:7b-instruct`
4. Set Up Python Virtual Environment: `python -m venv venv`, `source venv/bin/activate`
5. Install dependencies: `pip install -r requirements.txt`
6. Run Ollama: `ollama serve` (stop existing instances with `pkill -9 -f Ollama`)
7. Start the game: `python main.py`

## Commands
- `go [direction]`: Move in the game.
- `use [item]`: Use an item.
- `talk to sidekick`: Get advice.
- `voice`: Speak an action.
- `image [path]`: Introduce an image (uses qwen2:7b-instruct as fallback).
- `help`: Show commands.
- `exit`: Quit the game.

## Example Gameplay
Starting game, generating intro...
=== Adventure Game ===
Curiosity piqued, the player questions the origin of the bear cub...
What do you do? (or say 'voice', 'image [path]', 'help', 'exit'): voice
Recording for 5 seconds...
Recording finished.
You said: go north
The player, with Cubby padding alongside, ventures north...


## Notes
- `qwen-vl` not available; used `qwen2:7b-instruct`. For image processing, see custom `qwen-vl-custom` setup in code comments.
- Ensure microphone permissions for voice input on macOS.
- FP16 warning from Whisper is normal on CPU.

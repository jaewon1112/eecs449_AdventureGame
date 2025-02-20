# Adventure Game
A text-based adventure game using Ollama, LangChain, and Whisper.

## Setup
1. Install Ollama: https://ollama.ai/
2. Pull models: `ollama pull deepseek-r1`, `ollama pull qwen2:7b-instruct`
3. Activate virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run Ollama: `ollama serve` (stop existing instances with `pkill -9 -f Ollama`)
6. Start the game: `python main.py`

## Commands
- `go [direction]`: Move in the game.
- `use [item]`: Use an item.
- `talk to sidekick`: Get advice.
- `voice`: Speak an action.
- `image [path]`: Introduce an image (uses qwen2:7b-instruct as fallback).
- `help`: Show commands.
- `exit`: Quit the game.

## Notes
- `qwen-vl` not available; used `qwen2:7b-instruct`. For image processing, see custom `qwen-vl-custom` setup in code comments.
- Ensure microphone permissions for voice input on macOS.
- FP16 warning from Whisper is normal on CPU.
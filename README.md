# Hangman Game

Welcome to the Hangman Game! This is a classic word-guessing game where you'll try to figure out a hidden word one letter at a time. Be careful though, you only have a limited number of incorrect guesses before the hangman is complete!

# Getting started
Follow all steps to run Hangman game on your local machine

## Installation

1. Clone the repository to your local machine.
```
https://github.com/liniusst/hangman.git
```

2. Create and activate virtual environment:
```
python3 -m venv .venv

For macOS/Linux:
source .venv/bin/activate

For Windows:
source .venv/Scripts/ativate
```

3. Prepare virtual environment for game app:
```
pip install -r requirements.txt
```

## Run directly

1. Start backend webservice (FastAPI):
```
cd backend
uvicorn main:app --host 127.0.0.1 --port 1337
```

2. Start frontend webservice (Flask):
```
cd frontend
flask run --host 127.0.0.1 --port 1338
```

3. Visit website game app:
```
http://127.0.0.1:1338/
```

## Run with Docker

## How to play
- Visit game website;
- Register new account or log in to older one;
- Press Start game button;
- Guess letters to reveal the hidden game word;
- Each incorrect guess takes -1 trie from you;
- On play page, you need tracck your guesses and bad tries.

### Good luck!



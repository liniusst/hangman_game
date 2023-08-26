# Hangman Game

![alt text](docs/hangman-game.png?raw=true)


Welcome to the Hangman Game! This is a classic word-guessing game where you'll try to figure out a hidden word one letter at a time. Be careful though, you only have a limited number of incorrect guesses before the hangman is complete!

# Getting started
Follow all steps to run Hangman game on your local machine or use Docker

## Run directly on your machine
### Prepare machine for game

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

### Configure database and run webservices

1. Set database for local run
```
# backend/database.py

SQLALCHEMY_DATABASE_URL = "sqlite:///../sql_app.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
```

2. Start backend webservice (FastAPI):
```
cd backend
uvicorn backend:app --host 127.0.0.1 --port 1337
```

3. Start frontend webservice (Flask):
```
cd frontend
export FLASK_APP=frontend/app.py
flask run --host 127.0.0.1 --port 1338
```

4. Visit Hangman game website and FastAPI:
```
Game website: http://127.0.0.1:1338/
FastAPI: http://127.0.0.1:1337/docs
```

## Run with Docker
### Prepare game files for Dockerization
1. Clone the repository to your local machine.
```
https://github.com/liniusst/hangman.git
```

2. Set database for Docker (Postgres)
```
# backend/database.py

SQLALCHEMY_DATABASE_URL = ("postgresql://hangman:h4ngm4npa55w0rd@hangman_database:5432/hangman_db")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
```

3. Build game image
```
docker-compose build --no-cache
```

4. Run Docker
```
docker-compose up
```

5. Visit Hangman game website and FastAPI:
```
Game website: http://127.0.0.1:1338/
FastAPI: http://127.0.0.1:1337/docs
```


## How to play
- Visit game website;
- Register new account or log in to older one;
- Press Start game button;
- Guess letters to reveal the hidden game word;
- Each incorrect guess takes -1 trie from you;
- On play page, you need tracck your guesses and bad tries.

### Good luck!



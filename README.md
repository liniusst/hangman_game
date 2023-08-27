# Hangman Game

![alt text](docs/hangman-game.png?raw=true)


Welcome to the Hangman Game! This is a classic word-guessing game where you'll try to figure out a hidden word one letter at a time. Be careful though, you only have a limited number of incorrect guesses before the hangman is complete!

# Getting started
Follow all steps to run Hangman game on Docker.

- Backend: FastAPI
- Frontend: Flask
- Database: PostgreSQL

## Run with Docker

1. Clone the repository to your local machine.
```
https://github.com/liniusst/hangman.git
```

2. Build game image
```
docker-compose build --no-cache
```

3. Run Docker
```
docker-compose up
```

4. Visit Hangman game website and FastAPI:
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



Learning Django - Week 9 Assignment - Random Word Generator
Create a new Django app called 'random_word'. Your template will show a random word with 14 characters in length.

The first time you use this app, it should say 'attempt #1'. Each time you generate a new random keyword, it should increment the attempt figure. It's okay if your random word is not a real word.

When an http request is sent to, say, localhost:8000/random_word/reset, have it reset the counter for the attempt and redirect back to localhost:8000/random_word.
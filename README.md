# wordle_solver
## Helps solve https://powerlanguage.co.uk/wordle/ puzzles.
This Python3 program runs on the command line.
To play Wordle you provide an initial guess of the solution word. After you click the `Enter` button the letters of your guess will change to grey, yellow, or green. Assuming the solution word was 'abcde' and your initial guess was `axyez`. `x`, `y`, and `z` would turn grey, `e` would turn yellow, and `a` would turn green. I'm going to use `-b` for grey letters, `-y` for yellow letters, and `-g` for green letters. You'll notice that `-y` and `-g` are followed by a pattern the same size as your guess (and the solution). Include underscores to get the same size and the letters in the same position as your guess. You also need to provide a file of words (one per line) of possible solutions. On Unix and Unix-like systems (including macOS and Linux) this file is `/usr/share/dict/words`. I've provided the file `guesses.txt` which is a copy of this file.
```
python3 solver.py -b 'xyz' -y '____e' -g 'a____' guesses.txt
```
The program will output suitable words for your next guess. You can add a `-d` to get extra details about how it makes it decisions. It considers each word in the possible solutions file. If the word contains any of the grey letters it isn't output. If it contains green letters in same position it is output. If is has yellow letters in the same position it isn't output, otherwise it is output. Select a suitable output word for your next guess.
As you proceed with your guesses you might have yellow letters in different positions. You can include several `-y '<yellow letter pattern>'`. The program checks each pattern against the word it is considering.

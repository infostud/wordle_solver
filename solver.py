#!/usr/bin/env python3
# Geoff 2022-01-19
WORDLE_LEN = 5
class Wordle_Solver():
#
  def __init__(self, d, bl, yp, gp, wf):
    import string
    self.debug = d
# Collection of letters not in the Wordle
    self.grey_letters = set()
    self.grey_letters.update(bl)
# Pattern of letters found but not in the right position
    self.yellow_patterns = yp
# Pattern of letters found and in the right position
    self.green_pattern = gp
    words = []
    with open(wf) as wordfile:
      for line in wordfile:
        word = line.strip()
        if len(word) == WORDLE_LEN and word[0] in string.ascii_lowercase:
          words.append(word)
          #print('|' + word + '|')
    self.good_list = words
#
  def has_grey_letters(self, consider):
    found: bool = False
    assert len(consider) == WORDLE_LEN
    for i in range(0, WORDLE_LEN):
      if consider[i] in self.grey_letters:
        found = True
    if not found and self.debug:
      print(consider, "grey:", self.grey_letters, "dropped")
    return found
#
  def matches_yellow_patterns(self, consider):
    match: Bool = False
    if len(self.yellow_patterns) == 0:
      return match
    for p in self.yellow_patterns:
      match = match or self.matches_yellow_pattern(consider, p)
    return match
#
  def matches_yellow_pattern(self, consider, pattern):
    match: int = 0
    unique_letters: list = []
    assert len(consider) == WORDLE_LEN
    for i in range(0, WORDLE_LEN):
      if pattern[i] != '_' \
        and pattern[i] not in unique_letters:
        unique_letters.append(pattern[i])
      # Character not in this yellow pattern
    unique_length = len(unique_letters)
    i = 0
    while i < WORDLE_LEN:
      if consider[i] == pattern[i]:
        if self.debug:
          print(consider[i], "same", self.yellow_patterns)
      elif consider[i] in unique_letters:
        if self.debug:
          print(consider[i], "in", unique_letters)
        match += 1 # found in a different position
        if self.debug:
          print(consider[i], "contained in", unique_letters)
        del unique_letters[unique_letters.index(consider[i])]
      i += 1
    if self.debug:
      print(consider, "yellow:", self.yellow_patterns, "dropped")
    return match == unique_length
#
  def matches_green_pattern(self, consider):
    match: int = 0
    green_length = 0
    for i in range(0, WORDLE_LEN):
      if self.green_pattern[i] != '_':
        green_length += 1
      if consider[i] == self.green_pattern[i]:
        match += 1
    if match != green_length and self.debug:
      print(consider, "green:", self.green_pattern, "dropped")
    return match == green_length
#
  def print_candidates(self):
    import string
    possible = ""
    for consider in self.good_list:
  # A word is a possible solution
  #   if it doesn't have any letters in the black letters
      if not self.has_grey_letters(consider):
        possible = consider
  #   if it contains all of the yellow letters in any position
      elif self.matches_yellow_patterns(consider):
        possible = consider
  # and all of the green letters in matching positions
      elif self.matches_green_pattern(consider):
        possible = consider
      else:
        pass
      if len(possible) > 0:
        print(possible)
  #
  def solve(self):
    guess = self.print_candidates()
#
def main(argv):
  import sys, getopt
  debug: Bool = False
  yellow_pattern = []
  try:
# Parse options, drop program name.
    opts, args = getopt.getopt(argv[1:], "hdb:y:g:w:")
  except getopt.GetoptError:
    print("Argument error(s)", opts, args)
    print(argv[0], " -h -d -b letters -y pattern -g pattern -w <wordfile>")
    sys.exit(2)
  if len(opts) < 1:
    print("No arguments", opts, args)
    print(argv[0], " -h -d -b letters -y pattern -g pattern -w <wordfile>")
    sys.exit(2)
  for opt, arg in opts:
    #print(opt, arg)
    if opt == "-h":
      print(argv[0], " -h -d -b letters -y pattern -g pattern -w <wordfile>")
      print("""-h prints this help. -d extra output
This program helps solve Wordle puzzles.
If the hidden solution was 'abcde' and a guess was 'axcye' then
-b <black/grey letters> a list of letters not found in the solution, eg 'xy'.
Note: a pattern must be the same size as the solution word and
an underscore '_' is ignored in a position in the pattern.
-y <yellow pattern> 
   (letters found in the solution but not in the correct position), eg 'bea__'.
Note: the yellow pattern can appear more than once,
eg -y '__c__' -y 'c___p' -y '__pic'
-g <green pattern> 
   (letters found in the solution and in the correct position), eg 'a_c_e'
Hint: 'b' could be in position 2 or 4. You've got to guess one more letter.
-w <wordfile> a list of words (each word on one line)
   hopefully containing the solution.""")
      sys.exit(0)
    elif opt == "-d":
      debug = True
    elif opt == "-b":
      grey_letters = arg
    elif opt == "-y":
      if len(arg) != WORDLE_LEN:
        print("Yellow pattern '", arg, "'length not", WORDLE_LEN)
        sys.exit(2)
      yellow_pattern.append(arg)
    elif opt == "-g":
      if len(arg) != WORDLE_LEN:
        print("Green pattern '", arg, "'length not", WORDLE_LEN)
        sys.exit(2)
      green_pattern = arg
    elif opt == "-w":
      wordsfile = arg
    else:
      print("Error in arguments:", argv, opts, args)
      sys.exit(2)
#
  wordle = Wordle_Solver(debug, grey_letters, yellow_pattern,
                         green_pattern, wordsfile)
  wordle.solve()
#
if __name__ == "__main__":
  import sys
  main(sys.argv)

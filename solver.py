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
    if bl:
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
    self.solution_list = words
#
  def has_grey_letters(self, consider):
    found: bool = False
    assert len(consider) == WORDLE_LEN
    for i in range(0, WORDLE_LEN):
      if consider[i] in self.grey_letters:
        found = True
        break # short-cut loop
    if found and self.debug:
      print(consider, "has one or more grey letters:",
            self.grey_letters, "dropped")
    return found
#
  def matches_yellow_patterns(self, consider):
    match: Bool = False
    if self.debug:
      print("Yellow patterns:", self.yellow_patterns)
    if len(self.yellow_patterns) > 0:
      for pattern in self.yellow_patterns:
        if self.debug:
          print(consider, '"', pattern, '"')
        match = match or self.matches_yellow_pattern(consider, pattern)
    return match
#
  def matches_yellow_pattern(self, consider, pattern):
    """
    Make a list of unique letters from the pattern and return False 
    if the word doesn't have any of these letters.
    Return False if the word does have one or more letters in the pattern
    but in the same position. The letters would be green.
    """
#
    matches: int = 0 # count of matches but not in the same position
    same_position: bool = False # Found a yellow letter in the same position
    assert len(consider) == WORDLE_LEN
    assert len(pattern) == WORDLE_LEN
    
    for i in range(0, WORDLE_LEN):
      if consider[i] == pattern[i]:
        if self.debug:
          print(consider[i], "in the same position", pattern,
                consider, "dropped")
        same_position = True
        break # short-circuit loop
    #
    if not same_position:
      unique_letters = set(pattern) # a set of unique letters from a string
      unique_letters.remove('_') # remove the fill character

      for i in range(0, WORDLE_LEN):
        if consider[i] in unique_letters:
          if self.debug:
            print(consider[i], "contained in", unique_letters)
          matches += 1 # found in a different position
      return matches > 0
    else:
      False
#
  def matches_green_pattern(self, consider):
    match: int = 0
    green_length: int = 0
    assert len(self.green_pattern) == WORDLE_LEN
    for i in range(0, WORDLE_LEN):
      if self.green_pattern[i] != '_':
        green_length += 1
        if consider[i] == self.green_pattern[i]:
          match += 1
    if match != green_length and self.debug:
      print(consider, "no green letters:", self.green_pattern, "dropped")
      return False
    else:
      return match == green_length
#
  def print_candidates(self):
    import string
    green: bool
    for consider in self.solution_list:
      if not self.has_grey_letters(consider):
        if self.matches_yellow_patterns(consider) \
           and self.matches_green_pattern(consider):
          print("Possible:", consider)
  #
  def solve(self):
    guess = self.print_candidates()
#
def main(argv):
  import sys, getopt
  debug: Bool = False
  grey_letters = ''
  yellow_pattern = ["_____"]
  #green_pattern = "_____"
  wordsfile = "/usr/share/dict/words"
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

#!/usr/bin/env python3
# Geoff 2021-01-23
#
def main():
  import argparse, solver
  ap = argparse.ArgumentParser(description="""
Help guess Wordle puzzles. Supply optional strings of letters, either
grey, yellow, or green.""")
  ap.add_argument("-v", "--verbosity", help="increase output verbosity",
                  default=0, action="count")
  ap.add_argument("-b", "--grey", help="grey letter string", type=str)
  ap.add_argument("-y", "--yellow", help="yellow letter pattern", type=str,
                  action="append") # allow several -y "pattern"
  ap.add_argument("-g", "--green", help="green letter pattern", type=str)
  ap.add_argument("-f", "--guessfile", default="guesses.txt", type=str,
                  help="file containings guesses")
  args = ap.parse_args()
  if args.verbosity:
    print("verbosity level", args.verbosity)
  if args.grey:
    print("grey:", len(args.grey), args.grey)
  if args.yellow:
    print("yellow:", len(args.yellow), args.yellow)
  if args.green:
    print("green:", len(args.green), args.green)
  if args.guessfile:
    print("guessfile:", args.guessfile)
#
  solve = solver.Wordle_Solver(args.verbosity,
          args.grey, args.yellow, args.green, args.guessfile)
  solve.solve()
#
if __name__ == "__main__":
  main()

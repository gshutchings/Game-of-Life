import game
import sys


if __name__ == "__main__":
   print(
   """
   Hello! Welcome to Conway's Game of Life.
   To add or delete pixels, right click on it. You can also drag.
   To move around the screen, left click and drag.
   To clear the screen, press c, and to fill it, press f.
   You can change the speed with the bar on the bottom.
   Feel free to resize the window.
   """
   )
   if len(sys.argv) > 1:
      rule = sys.argv[1]
   else:
      rule = ""
   game.run_game(rule)
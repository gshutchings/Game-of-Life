"""
We will keep all of the points in a set in order
to quickly check if a point is in it.
To pass time, we will create a set of every nearby
point, keeping track of how many original points
tried to add it (that is, how many points from the
original point list are adjacent to the new point).
"""


from collections import defaultdict


class Game:


   def __init__(self, born: list = [3], survive: list = [2, 3]) -> None:
       if born == [3] and survive == [2, 3]:
           self.points = {(-1, 0), (0, 1), (1, 1), (1, 0), (1, -1)} # Starts with a glider for Conway's Game of Life
       else:
           self.points = set() # All active points
       self.b = set(born)
       self.s = set(survive) # Sets, for fast lookup
       return
  
   def step(self) -> None:
       possible_points = set() # Every current point and all 8 neighbors
       neighbor_count = defaultdict(int) # Running total of how many neighbors a potential cell has


       for (pt1, pt2) in self.points:
           for dx, dy in [[-1, 1], [0, 1], [1, 1],
                          [-1, 0],         [1, 0],
                          [-1, -1],[0, -1],[1, -1]]:
               neighbor = (pt1 + dx, pt2 + dy)
               possible_points.add(neighbor)
               neighbor_count[neighbor] += 1


       new_points = set()
       for point in possible_points:
           if (point in self.points):
               if neighbor_count[point] in self.s:
                   new_points.add(point)
           else:
               if neighbor_count[point] in self.b:
                   new_points.add(point)
      
       self.points = new_points
       return

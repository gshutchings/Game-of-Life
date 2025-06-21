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

    def __init__(self, rule: str) -> None:
        born, survive = self.rule_parser(rule)
        if born == [3] and survive == [2, 3]:
            self.points = {(-1, 0), (0, 1), (1, 1), (1, 0), (1, -1)} # Starts with a glider for Conway's Game of Life
        elif born == [3, 6] and survive == [2, 3]:
            self.points = {(-1, 1), (1, -1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (0, -2), (-1, -2), (-2, -2), (-2, -1), (-2, 0)}
            # Replicator for highlife
        else:
            self.points = set() # All active points
        self.b = set(born)
        self.s = set(survive) # Sets, for fast lookup
        return
   
    @staticmethod
    def rule_parser(rule: str):
        if rule.count('/'):
            parts = rule.split('/')
            a = list(parts[0][1:])
            b = list(parts[1][1:])
            possible = list('0123456789')
            for x in a:
                assert(x in possible), "Could not interpret input as a rule. "
            for x in b:
                assert(x in possible), "Could not interpret input as a rule. "
            return list(map(int, a)), list(map(int, b))
        elif rule.count('way'): # Conway's Game of Life
            return [3], [2, 3]
        elif rule.count('ife'): # Highlife
            return [3, 6], [2, 3]
        elif rule.count('eed'): # Seeds
            return [2], []
        elif rule.count('igh'): # Day & Night
            return [3, 6, 7, 8], [3, 4, 6, 7, 8]
        elif rule.count('2x2'): # 2x2
            return [3, 6], [1, 2, 5]
        elif rule.count('out'): # Life without death
            return [3], [0, 1, 2, 3, 4, 5, 6, 7, 8]
        print("Could not interpret input. Defaulting to Conway's Game of Life. ")
        return [3], [2, 3]

  
    def step(self) -> None:
        possible_points = set() # Every current point and all 8 neighbors
        neighbor_count = defaultdict(int) # Running total of how many neighbors a potential cell has
        for (pt1, pt2) in self.points:
            for dx, dy in [[-1, 1], [0, 1], [1, 1],
                            [-1, 0], [0, 0], [1, 0],  # Includes itself in case it has no neighbors and self.s includes 0
                            [-1, -1],[0, -1],[1, -1]]:
                neighbor = (pt1 + dx, pt2 + dy)
                possible_points.add(neighbor)
                neighbor_count[neighbor] += 1
    

        new_points = set()
        for point in possible_points:
            if (point in self.points):
                if neighbor_count[point] - 1 in self.s:
                    new_points.add(point)
            else:
                if neighbor_count[point] in self.b:
                    new_points.add(point)
        for point in self.points:
            if neighbor_count[point] in self.s:
                new_points.add(point)
        
        self.points = new_points
        return

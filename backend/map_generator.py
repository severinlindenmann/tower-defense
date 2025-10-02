"""Map generator for grid-based tower defense game"""
import random
from typing import List, Tuple, Dict
from collections import deque


class MapGenerator:
    """Generates a grid-based map with path, terrain, and decorations"""
    
    def __init__(self, grid_size: int = 30):
        self.grid_size = grid_size
        self.grid = []
        self.path = []
        
    def generate_map(self) -> Dict:
        """Generate a new random map"""
        # Initialize grid with grass
        self.grid = [['grass' for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        # Generate winding path
        self.path = self._generate_path()
        
        # Mark path tiles
        for x, y in self.path:
            self.grid[y][x] = 'path'
        
        # Add terrain features
        self._add_rivers()
        self._add_mountains()
        self._add_decorations()
        
        return {
            'grid': self.grid,
            'path': self.path,
            'grid_size': self.grid_size,
            'cell_size': 20  # pixels per cell
        }
    
    def _generate_path(self) -> List[Tuple[int, int]]:
        """Generate a winding path from left to right"""
        path = []
        
        # Start position (left side, middle area)
        start_y = self.grid_size // 2 + random.randint(-3, 3)
        x, y = 0, start_y
        path.append((x, y))
        
        # Wind to the right
        while x < self.grid_size - 1:
            x += 1
            
            # Randomly move up or down
            if random.random() < 0.3:
                dy = random.choice([-1, 0, 1])
                y = max(1, min(self.grid_size - 2, y + dy))
            
            path.append((x, y))
            
            # Occasionally add extra segments for complexity
            if random.random() < 0.2 and x < self.grid_size - 1:
                for _ in range(random.randint(1, 2)):
                    dy = random.choice([-1, 0, 1])
                    y = max(1, min(self.grid_size - 2, y + dy))
                    path.append((x, y))
        
        return path
    
    def _add_rivers(self):
        """Add river tiles that can't have towers"""
        num_rivers = random.randint(2, 4)
        
        for _ in range(num_rivers):
            # Start from a random edge
            if random.random() < 0.5:
                # Vertical river
                x = random.randint(3, self.grid_size - 4)
                for y in range(self.grid_size):
                    if self.grid[y][x] != 'path':
                        self.grid[y][x] = 'river'
                        # Make it 2-3 tiles wide
                        if x + 1 < self.grid_size and self.grid[y][x + 1] != 'path':
                            self.grid[y][x + 1] = 'river'
            else:
                # Horizontal river
                y = random.randint(3, self.grid_size - 4)
                for x in range(self.grid_size):
                    if self.grid[y][x] != 'path':
                        self.grid[y][x] = 'river'
    
    def _add_mountains(self):
        """Add mountain tiles (elevated, can have towers)"""
        num_mountains = random.randint(3, 6)
        
        for _ in range(num_mountains):
            # Random cluster of mountains
            center_x = random.randint(2, self.grid_size - 3)
            center_y = random.randint(2, self.grid_size - 3)
            
            size = random.randint(2, 4)
            for dx in range(-size//2, size//2 + 1):
                for dy in range(-size//2, size//2 + 1):
                    x, y = center_x + dx, center_y + dy
                    if (0 <= x < self.grid_size and 0 <= y < self.grid_size and
                        self.grid[y][x] == 'grass' and random.random() < 0.7):
                        self.grid[y][x] = 'mountain'
    
    def _add_decorations(self):
        """Add decorative elements"""
        # Add some forest tiles
        for _ in range(random.randint(10, 20)):
            x = random.randint(0, self.grid_size - 1)
            y = random.randint(0, self.grid_size - 1)
            if self.grid[y][x] == 'grass':
                self.grid[y][x] = 'forest'
    
    def can_place_tower(self, x: int, y: int) -> bool:
        """Check if a tower can be placed at this position"""
        if not (0 <= x < self.grid_size and 0 <= y < self.grid_size):
            return False
        
        tile_type = self.grid[y][x]
        # Can place towers on grass, mountains, and forest
        # Cannot place on path or river
        return tile_type in ['grass', 'mountain', 'forest']
    
    def get_tile_type(self, x: int, y: int) -> str:
        """Get the tile type at a position"""
        if not (0 <= x < self.grid_size and 0 <= y < self.grid_size):
            return 'void'
        return self.grid[y][x]

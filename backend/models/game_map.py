from typing import List, Dict, Tuple, Set
import random
from enum import Enum


class TerrainType(Enum):
    PLAINS = "plains"
    MOUNTAIN = "mountain"
    LAKE = "lake"
    ROAD = "road"


class GameMap:
    """Manages the game map with terrain and pathfinding"""
    
    def __init__(self, grid_size: int = 20, cell_size: int = 30):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.terrain: List[List[TerrainType]] = []
        self.road_path: List[Tuple[int, int]] = []
        self.start_pos: Tuple[int, int] = (0, 0)
        self.end_pos: Tuple[int, int] = (0, 0)
        
        self._generate_map()
    
    def _generate_map(self):
        """Generate the entire map with road, mountains, and lakes"""
        # Initialize with plains
        self.terrain = [[TerrainType.PLAINS for _ in range(self.grid_size)] 
                       for _ in range(self.grid_size)]
        
        # Generate road
        self._generate_road()
        
        # Add mountains and lakes
        self._generate_terrain_features()
    
    def _generate_road(self):
        """Generate a random road from one side to another"""
        # Randomly choose start and end sides
        sides = ["top", "bottom", "left", "right"]
        start_side = random.choice(sides)
        
        # Remove opposite side from end choices for variety
        opposite = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}
        end_side = random.choice([s for s in sides if s != start_side])
        
        # Get start and end positions
        self.start_pos = self._get_edge_position(start_side)
        self.end_pos = self._get_edge_position(end_side)
        
        # Generate path using A* or simple pathfinding
        self.road_path = self._generate_path(self.start_pos, self.end_pos)
        
        # Mark road cells in terrain
        for x, y in self.road_path:
            if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                self.terrain[y][x] = TerrainType.ROAD
    
    def _get_edge_position(self, side: str) -> Tuple[int, int]:
        """Get a random position on the specified edge"""
        mid = self.grid_size // 2
        offset = random.randint(-3, 3)
        
        if side == "top":
            return (mid + offset, 0)
        elif side == "bottom":
            return (mid + offset, self.grid_size - 1)
        elif side == "left":
            return (0, mid + offset)
        else:  # right
            return (self.grid_size - 1, mid + offset)
    
    def _generate_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Generate a winding path from start to end"""
        path = [start]
        current = start
        
        # Use a random walk with bias towards the goal
        max_attempts = self.grid_size * 10
        attempts = 0
        
        while current != end and attempts < max_attempts:
            attempts += 1
            cx, cy = current
            ex, ey = end
            
            # Calculate direction to goal
            dx = 1 if ex > cx else (-1 if ex < cx else 0)
            dy = 1 if ey > cy else (-1 if ey < cy else 0)
            
            # Randomly choose to move in x or y direction (with bias towards goal)
            if random.random() < 0.7:  # 70% chance to move towards goal
                if abs(ex - cx) > abs(ey - cy):
                    next_pos = (cx + dx, cy)
                elif abs(ey - cy) > 0:
                    next_pos = (cx, cy + dy)
                else:
                    next_pos = (cx + dx, cy)
            else:
                # Random perpendicular movement for curves
                if dx != 0:
                    dy_rand = random.choice([-1, 0, 1])
                    next_pos = (cx + dx, cy + dy_rand)
                else:
                    dx_rand = random.choice([-1, 0, 1])
                    next_pos = (cx + dx_rand, cy + dy)
            
            # Validate position
            nx, ny = next_pos
            if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                if next_pos not in path or next_pos == end:
                    path.append(next_pos)
                    current = next_pos
        
        # If we didn't reach the end, connect directly
        if current != end:
            path.append(end)
        
        return path
    
    def _generate_terrain_features(self):
        """Add mountains and lakes to the map"""
        # Count non-road cells
        available_cells = []
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.terrain[y][x] != TerrainType.ROAD:
                    available_cells.append((x, y))
        
        # Add 3-5 mountain clusters
        num_mountain_clusters = random.randint(3, 5)
        for _ in range(num_mountain_clusters):
            self._add_terrain_cluster(TerrainType.MOUNTAIN, available_cells, cluster_size=3)
        
        # Add 2-4 lake clusters
        num_lake_clusters = random.randint(2, 4)
        for _ in range(num_lake_clusters):
            self._add_terrain_cluster(TerrainType.LAKE, available_cells, cluster_size=2)
    
    def _add_terrain_cluster(self, terrain_type: TerrainType, available_cells: List[Tuple[int, int]], cluster_size: int):
        """Add a cluster of terrain features"""
        if not available_cells:
            return
        
        # Pick a random starting point
        center = random.choice(available_cells)
        cx, cy = center
        
        # Add center
        if self.terrain[cy][cx] != TerrainType.ROAD:
            self.terrain[cy][cx] = terrain_type
        
        # Add neighboring cells
        for _ in range(cluster_size):
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < self.grid_size and 0 <= ny < self.grid_size:
                    if self.terrain[ny][nx] != TerrainType.ROAD and random.random() < 0.4:
                        self.terrain[ny][nx] = terrain_type
    
    def get_terrain(self, x: int, y: int) -> TerrainType:
        """Get terrain type at position"""
        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            return self.terrain[y][x]
        return TerrainType.PLAINS
    
    def can_place_tower(self, x: int, y: int) -> bool:
        """Check if a tower can be placed at this position"""
        if not (0 <= x < self.grid_size and 0 <= y < self.grid_size):
            return False
        return self.terrain[y][x] != TerrainType.ROAD
    
    def get_enemy_path_coords(self) -> List[Dict[str, float]]:
        """
        Get the path coordinates for enemies to follow
        Returns list of waypoints with pixel coordinates
        """
        waypoints = []
        for x, y in self.road_path:
            waypoints.append({
                "x": x + 0.5,  # Center of cell
                "y": y + 0.5
            })
        return waypoints
    
    def to_dict(self) -> Dict:
        """Convert map to dictionary for serialization"""
        return {
            "grid_size": self.grid_size,
            "cell_size": self.cell_size,
            "terrain": [[cell.value for cell in row] for row in self.terrain],
            "road_path": [{"x": x, "y": y} for x, y in self.road_path],
            "start_pos": {"x": self.start_pos[0], "y": self.start_pos[1]},
            "end_pos": {"x": self.end_pos[0], "y": self.end_pos[1]}
        }

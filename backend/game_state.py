"""Game state management for the tower defense game"""
from typing import Dict, List, Set, Any
from player import Player
from towers import create_tower, get_tower_cost
from enemies import create_enemy, get_wave_composition
from map_generator import MapGenerator


class GameState:
    """Manages the entire game state"""
    
    def __init__(self):
        self.players: Dict[str, Player] = {}
        self.enemies: List[Any] = []
        self.towers: List[Any] = []
        self.game_started = False
        self.wave_number = 0
        self.enemy_id_counter = 0
        self.tower_id_counter = 0
        
        # Generate map
        self.map_generator = MapGenerator(grid_size=30)
        self.map_data = self.map_generator.generate_map()
        
        # Player color management
        self.player_colors = [
            "#FF6B6B", "#4ECDC4", "#45B7D1", "#FFA07A", 
            "#98D8C8", "#F7DC6F", "#BB8FCE", "#85C1E2",
            "#F39C12", "#E74C3C", "#9B59B6", "#3498DB"
        ]
        self.used_colors: Set[str] = set()

    def get_player_color(self, player_id: str) -> str:
        """Assign a unique color to a player"""
        if player_id in self.players:
            return self.players[player_id].color
        
        # Find an unused color
        available_colors = [c for c in self.player_colors if c not in self.used_colors]
        if not available_colors:
            # If all colors used, generate a random one
            import random
            color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        else:
            color = available_colors[0]
        
        self.used_colors.add(color)
        return color

    def add_player(self, player_id: str, name: str):
        """Add a new player to the game"""
        if player_id not in self.players:
            color = self.get_player_color(player_id)
            self.players[player_id] = Player(player_id, name, color)

    def remove_player(self, player_id: str):
        """Remove a player from the game"""
        if player_id in self.players:
            # Free up the color
            self.used_colors.discard(self.players[player_id].color)
            
            # Remove player's towers
            self.towers = [t for t in self.towers if t.owner_id != player_id]
            
            del self.players[player_id]

    def place_tower(self, player_id: str, grid_x: int, grid_y: int, tower_type: str):
        """Place a tower for a player at grid coordinates"""
        # Check if player exists
        if player_id not in self.players:
            return False
        
        # Check if tile can have a tower
        if not self.map_generator.can_place_tower(grid_x, grid_y):
            return False
        
        # Check if there's already a tower at this position
        for tower in self.towers:
            if tower.grid_x == grid_x and tower.grid_y == grid_y:
                return False
        
        player = self.players[player_id]
        cost = get_tower_cost(tower_type)
        
        # Try to spend gold
        if player.spend_gold(cost):
            self.tower_id_counter += 1
            
            # Convert grid coordinates to pixel coordinates (center of cell)
            cell_size = self.map_data['cell_size']
            x = grid_x * cell_size + cell_size // 2
            y = grid_y * cell_size + cell_size // 2
            
            tower = create_tower(
                tower_type,
                self.tower_id_counter,
                x,
                y,
                player_id,
                player.color
            )
            # Add grid coordinates for easier checking
            tower.grid_x = grid_x
            tower.grid_y = grid_y
            
            self.towers.append(tower)
            player.tower_placed()
            return True
        
        return False

    def spawn_wave(self):
        """Spawn a new wave of enemies"""
        self.wave_number += 1
        composition = get_wave_composition(self.wave_number)
        spawned = []
        
        for enemy_type in composition:
            self.enemy_id_counter += 1
            enemy = create_enemy(enemy_type, self.enemy_id_counter, self.wave_number)
            self.enemies.append(enemy)
            spawned.append(enemy)
        
        return spawned

    def destroy_enemy(self, enemy_id: int, killer_player_id: str = None):
        """Remove an enemy and reward the player who killed it"""
        enemy = next((e for e in self.enemies if e.enemy_id == enemy_id), None)
        
        if enemy:
            reward = enemy.reward
            self.enemies = [e for e in self.enemies if e.enemy_id != enemy_id]
            
            # Reward only the killer
            if killer_player_id and killer_player_id in self.players:
                player = self.players[killer_player_id]
                player.add_gold(reward)
                player.add_score(reward)
                player.enemy_killed()
            
            return reward
        
        return 0

    def enemy_reached_end(self, enemy_id: int):
        """Handle enemy reaching the end"""
        self.enemies = [e for e in self.enemies if e.id != enemy_id]
        
        # All players lose a life
        for player in self.players.values():
            player.lose_life()

    def get_state(self) -> Dict[str, Any]:
        """Get the current game state as a dictionary"""
        return {
            "players": {pid: p.to_dict() for pid, p in self.players.items()},
            "enemies": [e.to_dict() for e in self.enemies],
            "towers": [t.to_dict() for t in self.towers],
            "game_started": self.game_started,
            "wave_number": self.wave_number,
        }
    
    def start_game(self):
        """Start the game"""
        self.game_started = True
    
    def get_tower_by_id(self, tower_id: int):
        """Get a tower by its ID"""
        return next((t for t in self.towers if t.id == tower_id), None)
    
    def get_enemy_by_id(self, enemy_id: int):
        """Get an enemy by its ID"""
        return next((e for e in self.enemies if e.id == enemy_id), None)

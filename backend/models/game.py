from typing import Dict, List, Optional
import time
import uuid
from models.game_map import GameMap, TerrainType
from models.player import Player
from models.tower import create_tower, Tower
from models.enemy import create_enemy, Enemy


class Game:
    """Main game class managing all game logic"""
    
    def __init__(self):
        self.game_map = GameMap(grid_size=20, cell_size=30)
        self.players: Dict[str, Player] = {}
        self.towers: Dict[str, Tower] = {}
        self.enemies: Dict[str, Enemy] = {}
        
        # Wave system
        self.current_wave = 0
        self.wave_in_progress = False
        self.wave_start_time = 0
        self.time_between_waves = 10.0  # seconds
        self.last_wave_end_time = time.time()
        
        # Enemy spawning
        self.enemies_to_spawn: List[Dict] = []
        self.last_spawn_time = 0
        self.spawn_interval = 1.0  # seconds between spawns
        
        # Game state
        self.game_started = False
        self.game_over = False
        self.last_update_time = time.time()
        
        # Attacks (for animation)
        self.recent_attacks: List[Dict] = []
    
    def add_player(self, player_id: str):
        """Add a player to the game"""
        if player_id not in self.players:
            self.players[player_id] = Player(player_id)
    
    def remove_player(self, player_id: str):
        """Remove a player from the game"""
        if player_id in self.players:
            del self.players[player_id]
    
    def start_game(self):
        """Start the game"""
        if not self.game_started:
            self.game_started = True
            self.last_update_time = time.time()
            self.start_next_wave()
    
    def start_next_wave(self):
        """Start the next wave of enemies"""
        self.current_wave += 1
        self.wave_in_progress = True
        self.wave_start_time = time.time()
        
        # Generate enemies for this wave
        self.enemies_to_spawn = self._generate_wave_enemies()
        self.last_spawn_time = time.time()
    
    def _generate_wave_enemies(self) -> List[Dict]:
        """Generate enemy spawn queue for current wave"""
        enemies_queue = []
        base_count = 5 + self.current_wave * 2
        
        # Determine enemy composition based on wave number
        for i in range(base_count):
            spawn_time = i * 1.5  # 1.5 seconds between spawns
            
            # Enemy type distribution changes with waves
            if self.current_wave <= 2:
                # Early waves: mostly fast enemies
                enemy_type = "fast" if i % 3 != 0 else "tank"
            elif self.current_wave <= 5:
                # Mid waves: mix of all types
                types = ["fast", "fast", "tank", "flying"]
                enemy_type = types[i % len(types)]
            else:
                # Late waves: more tanks and flying
                types = ["fast", "tank", "tank", "flying", "flying"]
                enemy_type = types[i % len(types)]
            
            enemies_queue.append({
                "type": enemy_type,
                "spawn_time": spawn_time
            })
        
        return enemies_queue
    
    def place_tower(self, player_id: str, x: int, y: int, tower_type: str) -> Dict:
        """
        Place a tower on the map
        Returns result dict with success status and message
        """
        if player_id not in self.players:
            return {"success": False, "message": "Player not found"}
        
        player = self.players[player_id]
        
        # Check if position is valid
        if not self.game_map.can_place_tower(x, y):
            return {"success": False, "message": "Cannot place tower on road"}
        
        # Check if tower already exists at position
        for tower in self.towers.values():
            if tower.x == x and tower.y == y:
                return {"success": False, "message": "Tower already exists here"}
        
        # Get terrain type
        terrain = self.game_map.get_terrain(x, y)
        
        # Create tower
        tower_id = str(uuid.uuid4())
        tower = create_tower(tower_type, x, y, terrain, tower_id)
        
        # Check if player has enough money
        if not player.spend_money(tower.cost):
            return {"success": False, "message": f"Not enough money (need {tower.cost})"}
        
        # Place tower
        self.towers[tower_id] = tower
        player.build_tower()
        
        return {
            "success": True,
            "message": "Tower placed",
            "tower": tower.to_dict()
        }
    
    def upgrade_tower(self, player_id: str, tower_id: str, upgrade_path: str) -> Dict:
        """
        Upgrade a tower
        Returns result dict with success status
        """
        if player_id not in self.players:
            return {"success": False, "message": "Player not found"}
        
        if tower_id not in self.towers:
            return {"success": False, "message": "Tower not found"}
        
        player = self.players[player_id]
        tower = self.towers[tower_id]
        
        upgrade_cost = tower.get_upgrade_cost()
        
        if not player.spend_money(upgrade_cost):
            return {"success": False, "message": f"Not enough money (need {upgrade_cost})"}
        
        if not tower.upgrade(upgrade_path):
            return {"success": False, "message": "Cannot upgrade further"}
        
        return {
            "success": True,
            "message": "Tower upgraded",
            "tower": tower.to_dict()
        }
    
    def update(self, delta_time: float = None):
        """
        Update game state
        Called regularly to advance game logic
        """
        if not self.game_started or self.game_over:
            return
        
        current_time = time.time()
        if delta_time is None:
            delta_time = current_time - self.last_update_time
        self.last_update_time = current_time
        
        # Clear old attacks
        self.recent_attacks = []
        
        # Spawn enemies
        if self.wave_in_progress and self.enemies_to_spawn:
            self._spawn_enemies(current_time)
        
        # Move enemies
        self._update_enemies(delta_time, current_time)
        
        # Tower attacks
        self._update_towers(current_time)
        
        # Check wave completion
        if self.wave_in_progress and not self.enemies_to_spawn and not self.enemies:
            self._end_wave()
        
        # Start next wave if ready
        if not self.wave_in_progress:
            time_since_wave = current_time - self.last_wave_end_time
            if time_since_wave >= self.time_between_waves:
                self.start_next_wave()
        
        # Check game over
        self._check_game_over()
    
    def _spawn_enemies(self, current_time: float):
        """Spawn enemies from the queue"""
        wave_time = current_time - self.wave_start_time
        
        # Spawn enemies whose time has come
        enemies_to_remove = []
        for enemy_data in self.enemies_to_spawn:
            if wave_time >= enemy_data["spawn_time"]:
                enemy_id = str(uuid.uuid4())
                path = self.game_map.get_enemy_path_coords()
                enemy = create_enemy(enemy_data["type"], enemy_id, path, current_time)
                self.enemies[enemy_id] = enemy
                enemies_to_remove.append(enemy_data)
        
        for enemy_data in enemies_to_remove:
            self.enemies_to_spawn.remove(enemy_data)
    
    def _update_enemies(self, delta_time: float, current_time: float):
        """Update all enemies"""
        enemies_to_remove = []
        
        for enemy_id, enemy in self.enemies.items():
            if not enemy.is_alive:
                enemies_to_remove.append(enemy_id)
                # Reward all players
                for player in self.players.values():
                    player.defeat_enemy(enemy.reward)
                continue
            
            # Move enemy
            reached_end = enemy.move(delta_time)
            
            if reached_end:
                enemies_to_remove.append(enemy_id)
                # Enemy reached end - damage all players
                for player in self.players.values():
                    player.lose_life(enemy.damage)
        
        # Remove dead/finished enemies
        for enemy_id in enemies_to_remove:
            if enemy_id in self.enemies:
                del self.enemies[enemy_id]
    
    def _update_towers(self, current_time: float):
        """Update all towers and handle attacks"""
        enemies_list = [e for e in self.enemies.values() if e.is_alive]
        
        for tower in self.towers.values():
            attack_result = tower.attack(enemies_list, current_time)
            if attack_result:
                self.recent_attacks.append(attack_result)
    
    def _end_wave(self):
        """End the current wave"""
        self.wave_in_progress = False
        self.last_wave_end_time = time.time()
        
        # Bonus money for completing wave
        for player in self.players.values():
            player.add_money(50 + self.current_wave * 10)
            player.add_points(100)
    
    def _check_game_over(self):
        """Check if game is over"""
        if all(not player.is_active for player in self.players.values()):
            self.game_over = True
    
    def get_time_to_next_wave(self) -> float:
        """Get seconds until next wave"""
        if self.wave_in_progress:
            return 0
        
        current_time = time.time()
        time_since_wave = current_time - self.last_wave_end_time
        return max(0, self.time_between_waves - time_since_wave)
    
    def to_dict(self) -> Dict:
        """Convert game state to dictionary for serialization"""
        return {
            "game_map": self.game_map.to_dict(),
            "players": {pid: player.to_dict() for pid, player in self.players.items()},
            "towers": {tid: tower.to_dict() for tid, tower in self.towers.items()},
            "enemies": {eid: enemy.to_dict() for eid, enemy in self.enemies.items()},
            "current_wave": self.current_wave,
            "wave_in_progress": self.wave_in_progress,
            "time_to_next_wave": self.get_time_to_next_wave(),
            "game_started": self.game_started,
            "game_over": self.game_over,
            "recent_attacks": self.recent_attacks
        }

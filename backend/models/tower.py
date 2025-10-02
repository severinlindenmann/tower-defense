from typing import List, Dict, Optional, Tuple
from enum import Enum
import math


class TerrainType(Enum):
    PLAINS = "plains"
    MOUNTAIN = "mountain"
    LAKE = "lake"
    ROAD = "road"


class TowerType(Enum):
    BASIC = "basic"
    SNIPER = "sniper"
    CANNON = "cannon"
    AOE = "aoe"


class Tower:
    """Base tower class"""
    
    def __init__(self, x: int, y: int, terrain: TerrainType, tower_id: str):
        self.id = tower_id
        self.x = x
        self.y = y
        self.terrain = terrain
        self.level = 1
        self.upgrade_path = []
        self.last_attack_time = 0
        self.target = None
        
        # Base stats (will be modified by subclasses and terrain)
        self.base_damage = 10
        self.base_range = 3
        self.base_attack_speed = 1.0  # attacks per second
        self.cost = 100
        
        self._apply_terrain_bonuses()
    
    def _apply_terrain_bonuses(self):
        """Apply terrain-specific bonuses"""
        if self.terrain == TerrainType.MOUNTAIN:
            self.base_range *= 1.5  # Long range on mountains
            self.base_damage *= 0.7  # Lower damage
        elif self.terrain == TerrainType.LAKE:
            self.base_damage *= 1.5  # High damage on lakes
            self.base_attack_speed *= 0.6  # Slower attack speed
    
    @property
    def damage(self) -> float:
        return self.base_damage * (1 + 0.2 * (self.level - 1))
    
    @property
    def range(self) -> float:
        return self.base_range * (1 + 0.1 * (self.level - 1))
    
    @property
    def attack_speed(self) -> float:
        return self.base_attack_speed * (1 + 0.15 * (self.level - 1))
    
    @property
    def attack_cooldown(self) -> float:
        """Time between attacks in seconds"""
        return 1.0 / self.attack_speed
    
    def can_attack(self, current_time: float) -> bool:
        """Check if tower can attack based on cooldown"""
        return (current_time - self.last_attack_time) >= self.attack_cooldown
    
    def get_distance(self, enemy_x: float, enemy_y: float) -> float:
        """Calculate distance to an enemy"""
        return math.sqrt((self.x - enemy_x) ** 2 + (self.y - enemy_y) ** 2)
    
    def is_in_range(self, enemy_x: float, enemy_y: float) -> bool:
        """Check if enemy is in range"""
        return self.get_distance(enemy_x, enemy_y) <= self.range
    
    def attack(self, enemies: List, current_time: float) -> Optional[Dict]:
        """
        Attack enemies in range
        Returns attack info if attack happened, None otherwise
        """
        if not self.can_attack(current_time):
            return None
        
        # Find enemies in range
        targets = [e for e in enemies if e.is_alive and self.is_in_range(e.x, e.y)]
        
        if not targets:
            return None
        
        # Attack logic (implemented by subclasses)
        attack_result = self._perform_attack(targets, current_time)
        
        if attack_result:
            self.last_attack_time = current_time
        
        return attack_result
    
    def _perform_attack(self, targets: List, current_time: float) -> Optional[Dict]:
        """Override in subclasses"""
        if targets:
            target = targets[0]  # Attack first enemy
            target.take_damage(self.damage)
            return {
                "tower_id": self.id,
                "type": "single",
                "target": {"x": target.x, "y": target.y, "enemy_id": target.id},
                "damage": self.damage
            }
        return None
    
    def upgrade(self, path: str = "damage") -> bool:
        """Upgrade tower"""
        if self.level >= 5:
            return False
        
        self.level += 1
        self.upgrade_path.append(path)
        
        # Apply specific upgrades based on path
        if path == "damage":
            self.base_damage *= 1.3
        elif path == "range":
            self.base_range *= 1.3
        elif path == "speed":
            self.base_attack_speed *= 1.3
        
        return True
    
    def get_upgrade_cost(self) -> int:
        """Calculate upgrade cost"""
        return int(self.cost * 0.5 * self.level)
    
    def to_dict(self) -> Dict:
        """Convert tower to dictionary for serialization"""
        return {
            "id": self.id,
            "type": self.__class__.__name__.lower().replace("tower", ""),
            "x": self.x,
            "y": self.y,
            "terrain": self.terrain.value,
            "level": self.level,
            "damage": self.damage,
            "range": self.range,
            "attack_speed": self.attack_speed,
            "upgrade_path": self.upgrade_path,
            "cost": self.cost
        }


class BasicTower(Tower):
    """Standard balanced tower"""
    
    def __init__(self, x: int, y: int, terrain: TerrainType, tower_id: str):
        super().__init__(x, y, terrain, tower_id)
        self.base_damage = 10
        self.base_range = 3
        self.base_attack_speed = 1.0
        self.cost = 100
        self._apply_terrain_bonuses()


class SniperTower(Tower):
    """Long range, low damage tower (best on mountains)"""
    
    def __init__(self, x: int, y: int, terrain: TerrainType, tower_id: str):
        super().__init__(x, y, terrain, tower_id)
        self.base_damage = 8
        self.base_range = 5
        self.base_attack_speed = 0.5
        self.cost = 150
        self._apply_terrain_bonuses()
    
    def _perform_attack(self, targets: List, current_time: float) -> Optional[Dict]:
        """Sniper targets the furthest enemy"""
        if targets:
            # Find enemy furthest along the path
            target = max(targets, key=lambda e: e.distance_traveled)
            target.take_damage(self.damage)
            return {
                "tower_id": self.id,
                "type": "sniper",
                "target": {"x": target.x, "y": target.y, "enemy_id": target.id},
                "damage": self.damage
            }
        return None


class CannonTower(Tower):
    """High damage, slow attack tower (best on lakes)"""
    
    def __init__(self, x: int, y: int, terrain: TerrainType, tower_id: str):
        super().__init__(x, y, terrain, tower_id)
        self.base_damage = 25
        self.base_range = 2.5
        self.base_attack_speed = 0.4
        self.cost = 200
        self._apply_terrain_bonuses()


class AoETower(Tower):
    """Area of effect tower - attacks multiple enemies"""
    
    def __init__(self, x: int, y: int, terrain: TerrainType, tower_id: str):
        super().__init__(x, y, terrain, tower_id)
        self.base_damage = 6
        self.base_range = 2.5
        self.base_attack_speed = 0.8
        self.aoe_radius = 1.5
        self.cost = 250
        self._apply_terrain_bonuses()
    
    def _perform_attack(self, targets: List, current_time: float) -> Optional[Dict]:
        """AoE attacks all enemies in range"""
        if targets:
            # Attack all targets in range
            hit_enemies = []
            for target in targets[:5]:  # Max 5 enemies
                target.take_damage(self.damage)
                hit_enemies.append({
                    "x": target.x,
                    "y": target.y,
                    "enemy_id": target.id
                })
            
            return {
                "tower_id": self.id,
                "type": "aoe",
                "targets": hit_enemies,
                "damage": self.damage,
                "radius": self.aoe_radius
            }
        return None


def create_tower(tower_type: str, x: int, y: int, terrain: TerrainType, tower_id: str) -> Tower:
    """Factory function to create towers"""
    tower_classes = {
        "basic": BasicTower,
        "sniper": SniperTower,
        "cannon": CannonTower,
        "aoe": AoETower
    }
    
    tower_class = tower_classes.get(tower_type.lower(), BasicTower)
    return tower_class(x, y, terrain, tower_id)

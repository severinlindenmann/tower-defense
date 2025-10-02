from typing import List, Dict, Optional
from enum import Enum
import math


class EnemyType(Enum):
    FAST = "fast"
    TANK = "tank"
    FLYING = "flying"


class Enemy:
    """Base enemy class"""
    
    def __init__(self, enemy_id: str, path: List[Dict[str, float]], spawn_time: float):
        self.id = enemy_id
        self.path = path  # List of waypoints [{x, y}, ...]
        self.current_waypoint_index = 0
        self.x = path[0]["x"] if path else 0
        self.y = path[0]["y"] if path else 0
        self.spawn_time = spawn_time
        self.is_alive = True
        self.distance_traveled = 0
        
        # Base stats
        self.max_health = 100
        self.current_health = self.max_health
        self.speed = 1.0  # cells per second
        self.reward = 10  # Money earned when defeated
        self.damage = 1  # Damage to player if reaches end
        
        # Resistances (0-1, where 1 = immune, 0 = normal damage)
        self.resistances = {
            "basic": 0,
            "sniper": 0,
            "cannon": 0,
            "aoe": 0
        }
    
    @property
    def health_percentage(self) -> float:
        """Get health as percentage"""
        return self.current_health / self.max_health if self.max_health > 0 else 0
    
    def take_damage(self, damage: float, tower_type: str = "basic") -> bool:
        """
        Apply damage to enemy
        Returns True if enemy died
        """
        if not self.is_alive:
            return False
        
        # Apply resistance
        resistance = self.resistances.get(tower_type, 0)
        actual_damage = damage * (1 - resistance)
        
        self.current_health -= actual_damage
        
        if self.current_health <= 0:
            self.is_alive = False
            self.current_health = 0
            return True
        
        return False
    
    def move(self, delta_time: float) -> bool:
        """
        Move enemy along path
        Returns True if reached end of path
        """
        if not self.is_alive or self.current_waypoint_index >= len(self.path):
            return True
        
        distance_to_move = self.speed * delta_time
        self.distance_traveled += distance_to_move
        
        while distance_to_move > 0 and self.current_waypoint_index < len(self.path):
            target = self.path[self.current_waypoint_index]
            dx = target["x"] - self.x
            dy = target["y"] - self.y
            distance_to_waypoint = math.sqrt(dx ** 2 + dy ** 2)
            
            if distance_to_waypoint <= distance_to_move:
                # Reached waypoint
                self.x = target["x"]
                self.y = target["y"]
                distance_to_move -= distance_to_waypoint
                self.current_waypoint_index += 1
                
                # Check if reached end
                if self.current_waypoint_index >= len(self.path):
                    return True
            else:
                # Move towards waypoint
                if distance_to_waypoint > 0:
                    ratio = distance_to_move / distance_to_waypoint
                    self.x += dx * ratio
                    self.y += dy * ratio
                distance_to_move = 0
        
        return False
    
    def to_dict(self) -> Dict:
        """Convert enemy to dictionary for serialization"""
        return {
            "id": self.id,
            "type": self.__class__.__name__.lower().replace("enemy", ""),
            "x": self.x,
            "y": self.y,
            "health": self.current_health,
            "max_health": self.max_health,
            "health_percentage": self.health_percentage,
            "is_alive": self.is_alive,
            "speed": self.speed,
            "distance_traveled": self.distance_traveled
        }


class FastEnemy(Enemy):
    """Low health, high speed enemy"""
    
    def __init__(self, enemy_id: str, path: List[Dict[str, float]], spawn_time: float):
        super().__init__(enemy_id, path, spawn_time)
        self.max_health = 50
        self.current_health = self.max_health
        self.speed = 2.5
        self.reward = 8
        self.damage = 1
        
        # Weak to AoE, resistant to sniper
        self.resistances = {
            "basic": 0,
            "sniper": 0.3,
            "cannon": 0,
            "aoe": -0.2  # Takes extra damage
        }


class TankEnemy(Enemy):
    """High health, slow speed enemy"""
    
    def __init__(self, enemy_id: str, path: List[Dict[str, float]], spawn_time: float):
        super().__init__(enemy_id, path, spawn_time)
        self.max_health = 300
        self.current_health = self.max_health
        self.speed = 0.6
        self.reward = 25
        self.damage = 3
        
        # Resistant to basic, weak to cannon
        self.resistances = {
            "basic": 0.3,
            "sniper": 0.1,
            "cannon": -0.3,  # Takes extra damage
            "aoe": 0.2
        }


class FlyingEnemy(Enemy):
    """Flying enemy - special properties"""
    
    def __init__(self, enemy_id: str, path: List[Dict[str, float]], spawn_time: float):
        super().__init__(enemy_id, path, spawn_time)
        self.max_health = 80
        self.current_health = self.max_health
        self.speed = 1.8
        self.reward = 15
        self.damage = 2
        
        # Takes reduced damage from all towers except sniper
        self.resistances = {
            "basic": 0.5,
            "sniper": 0,  # Sniper is good against flying
            "cannon": 0.6,
            "aoe": 0.4
        }


def create_enemy(enemy_type: str, enemy_id: str, path: List[Dict[str, float]], spawn_time: float) -> Enemy:
    """Factory function to create enemies"""
    enemy_classes = {
        "fast": FastEnemy,
        "tank": TankEnemy,
        "flying": FlyingEnemy
    }
    
    enemy_class = enemy_classes.get(enemy_type.lower(), Enemy)
    return enemy_class(enemy_id, path, spawn_time)

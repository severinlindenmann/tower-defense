"""Tower classes for the tower defense game"""
from typing import Dict, Any


class Tower:
    """Base tower class"""
    
    def __init__(self, tower_id: int, x: int, y: int, owner_id: str, owner_color: str):
        self.tower_id = tower_id
        self.x = x
        self.y = y
        self.owner_id = owner_id
        self.owner_color = owner_color
        self.tower_type = "basic"
        self.damage = 10
        self.range = 100
        self.fire_rate = 1.0
        self.cost = 100
        self.last_fire = 0
        self.splash_radius = 0
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert tower to dictionary for JSON serialization"""
        return {
            "id": self.tower_id,
            "x": self.x,
            "y": self.y,
            "type": self.tower_type,
            "owner": self.owner_id,
            "owner_color": self.owner_color,
            "damage": self.damage,
            "range": self.range,
            "fire_rate": self.fire_rate,
        }


class BasicTower(Tower):
    """Balanced tower with moderate stats"""
    
    def __init__(self, tower_id: int, x: int, y: int, owner_id: str, owner_color: str):
        super().__init__(tower_id, x, y, owner_id, owner_color)
        self.tower_type = "basic"


class FastTower(Tower):
    """Fast firing tower with low damage"""
    
    def __init__(self, tower_id: int, x: int, y: int, owner_id: str, owner_color: str):
        super().__init__(tower_id, x, y, owner_id, owner_color)
        self.tower_type = "fast"
        self.damage = 5
        self.range = 90
        self.fire_rate = 0.6
        self.cost = 150


class HeavyTower(Tower):
    """High damage tower with slow fire rate"""
    
    def __init__(self, tower_id: int, x: int, y: int, owner_id: str, owner_color: str):
        super().__init__(tower_id, x, y, owner_id, owner_color)
        self.tower_type = "heavy"
        self.damage = 25
        self.range = 110
        self.fire_rate = 2.0
        self.cost = 200


class SniperTower(Tower):
    """Long range tower with high accuracy"""
    
    def __init__(self, tower_id: int, x: int, y: int, owner_id: str, owner_color: str):
        super().__init__(tower_id, x, y, owner_id, owner_color)
        self.tower_type = "sniper"
        self.damage = 40
        self.range = 200
        self.fire_rate = 2.5
        self.cost = 300


class SplashTower(Tower):
    """Area of effect damage tower"""
    
    def __init__(self, tower_id: int, x: int, y: int, owner_id: str, owner_color: str):
        super().__init__(tower_id, x, y, owner_id, owner_color)
        self.tower_type = "splash"
        self.damage = 8
        self.range = 80
        self.fire_rate = 1.5
        self.cost = 250
        self.splash_radius = 50
        
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["splash_radius"] = self.splash_radius
        return data


class FreezeTower(Tower):
    """Slows down enemies"""
    
    def __init__(self, tower_id: int, x: int, y: int, owner_id: str, owner_color: str):
        super().__init__(tower_id, x, y, owner_id, owner_color)
        self.tower_type = "freeze"
        self.damage = 3
        self.range = 100
        self.fire_rate = 1.2
        self.cost = 200
        self.slow_amount = 0.5
        self.slow_duration = 2.0
        
    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        data["slow_amount"] = self.slow_amount
        data["slow_duration"] = self.slow_duration
        return data


# Tower factory
TOWER_TYPES = {
    "basic": BasicTower,
    "fast": FastTower,
    "heavy": HeavyTower,
    "sniper": SniperTower,
    "splash": SplashTower,
    "freeze": FreezeTower,
}


def create_tower(tower_type: str, tower_id: int, x: int, y: int, 
                 owner_id: str, owner_color: str) -> Tower:
    """Factory function to create towers"""
    tower_class = TOWER_TYPES.get(tower_type, BasicTower)
    return tower_class(tower_id, x, y, owner_id, owner_color)


def get_tower_cost(tower_type: str) -> int:
    """Get the cost of a tower type"""
    tower_class = TOWER_TYPES.get(tower_type, BasicTower)
    temp_tower = tower_class(0, 0, 0, "", "")
    return temp_tower.cost

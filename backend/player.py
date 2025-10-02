"""Player class for the tower defense game"""
from typing import Dict, Any


class Player:
    """Represents a player in the game"""
    
    def __init__(self, player_id: str, name: str, color: str):
        self.id = player_id
        self.name = name
        self.color = color
        self.gold = 500
        self.lives = 20
        self.score = 0
        self.towers_placed = 0
        self.enemies_killed = 0
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert player to dictionary for JSON serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "gold": self.gold,
            "lives": self.lives,
            "score": self.score,
            "towers_placed": self.towers_placed,
            "enemies_killed": self.enemies_killed,
        }
    
    def add_gold(self, amount: int):
        """Add gold to player"""
        self.gold += amount
        
    def spend_gold(self, amount: int) -> bool:
        """Try to spend gold, returns True if successful"""
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False
    
    def add_score(self, points: int):
        """Add score points"""
        self.score += points
        
    def lose_life(self):
        """Lose a life"""
        self.lives = max(0, self.lives - 1)
        
    def is_alive(self) -> bool:
        """Check if player still has lives"""
        return self.lives > 0
    
    def tower_placed(self):
        """Increment tower placement counter"""
        self.towers_placed += 1
        
    def enemy_killed(self):
        """Increment enemy kill counter"""
        self.enemies_killed += 1

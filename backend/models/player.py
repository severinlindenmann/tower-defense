from typing import Dict, List


class Player:
    """Represents a player in the game"""
    
    def __init__(self, player_id: str):
        self.id = player_id
        self.money = 500  # Starting money
        self.points = 0
        self.lives = 20  # Game over when reaches 0
        self.towers_built = 0
        self.enemies_defeated = 0
        self.is_active = True
    
    def add_money(self, amount: int):
        """Add money to player"""
        self.money += amount
    
    def spend_money(self, amount: int) -> bool:
        """
        Spend money if player has enough
        Returns True if successful
        """
        if self.money >= amount:
            self.money -= amount
            return True
        return False
    
    def add_points(self, points: int):
        """Add points to player"""
        self.points += points
    
    def lose_life(self, amount: int = 1):
        """Lose lives"""
        self.lives -= amount
        if self.lives <= 0:
            self.lives = 0
            self.is_active = False
    
    def defeat_enemy(self, reward: int, points: int = None):
        """Called when player defeats an enemy"""
        self.add_money(reward)
        if points is None:
            points = reward  # Points equal to reward by default
        self.add_points(points)
        self.enemies_defeated += 1
    
    def build_tower(self):
        """Called when player builds a tower"""
        self.towers_built += 1
    
    def to_dict(self) -> Dict:
        """Convert player to dictionary for serialization"""
        return {
            "id": self.id,
            "money": self.money,
            "points": self.points,
            "lives": self.lives,
            "is_active": self.is_active,
            "towers_built": self.towers_built,
            "enemies_defeated": self.enemies_defeated
        }

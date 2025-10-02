from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import time
import logging
from typing import Dict
from game_state import GameState

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS middleware - Allow both ports
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global game state
game_state = GameState()

# Connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, client_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]

    async def broadcast(self, message: str):
        disconnected = []
        for client_id, connection in self.active_connections.items():
            try:
                await connection.send_text(message)
            except Exception:
                disconnected.append(client_id)
        
        for client_id in disconnected:
            self.disconnect(client_id)

manager = ConnectionManager()

# Game loop
async def game_loop():
    """Main game loop that runs continuously"""
    while True:
        await asyncio.sleep(0.1)  # 10 FPS tick rate
        
        current_time = time.time()
        
        # Update towers - check for targets and shoot
        for tower in game_state.towers:
            if current_time - tower.last_fire >= tower.fire_rate:
                # Find closest enemy in range
                closest_enemy = None
                min_distance = float('inf')
                
                for enemy in game_state.enemies:
                    if tower.tower_type == "sniper" and not enemy.is_flying:
                        continue  # Sniper only targets flying enemies
                    
                    dx = enemy.x - tower.x
                    dy = enemy.y - tower.y
                    distance = (dx * dx + dy * dy) ** 0.5
                    
                    if distance <= tower.range and distance < min_distance:
                        min_distance = distance
                        closest_enemy = enemy
                
                # Shoot at closest enemy
                if closest_enemy:
                    tower.last_fire = current_time
                    
                    if tower.tower_type == "splash":
                        # Splash damage to all enemies in radius
                        for enemy in game_state.enemies:
                            dx = enemy.x - closest_enemy.x
                            dy = enemy.y - closest_enemy.y
                            distance = (dx * dx + dy * dy) ** 0.5
                            if distance <= tower.splash_radius:
                                enemy.take_damage(tower.damage)
                    elif tower.tower_type == "freeze":
                        # Slow enemy and damage
                        closest_enemy.take_damage(tower.damage)
                        closest_enemy.slowed = True
                        closest_enemy.slow_duration = current_time + 2.0  # 2 second slow
                    else:
                        closest_enemy.take_damage(tower.damage)
                    
                    # Check if enemy died
                    if closest_enemy.hp <= 0:
                        game_state.destroy_enemy(closest_enemy.enemy_id, tower.owner_id)
        
        # Update enemies - move along path
        for enemy in game_state.enemies:
            # Check slow duration
            speed_modifier = 1.0
            if hasattr(enemy, 'slowed') and enemy.slowed:
                if hasattr(enemy, 'slow_duration') and current_time < enemy.slow_duration:
                    speed_modifier = 0.5
                else:
                    enemy.slowed = False
            
            # Move enemy
            if enemy.path_index < len(enemy.path):
                target = enemy.path[enemy.path_index]
                dx = target[0] - enemy.x
                dy = target[1] - enemy.y
                distance = (dx * dx + dy * dy) ** 0.5
                
                if distance < enemy.speed * speed_modifier:
                    enemy.path_index += 1
                    if enemy.path_index >= len(enemy.path):
                        # Enemy reached the end
                        for player in game_state.players.values():
                            player.lose_life()
                        game_state.enemies.remove(enemy)
                else:
                    enemy.x += (dx / distance) * enemy.speed * speed_modifier
                    enemy.y += (dy / distance) * enemy.speed * speed_modifier
        
        # Healer enemy special ability
        for enemy in game_state.enemies:
            if enemy.enemy_type == "healer" and current_time - getattr(enemy, 'last_heal', 0) >= 3.0:
                enemy.last_heal = current_time
                # Heal nearby enemies
                for other in game_state.enemies:
                    if other.enemy_id != enemy.enemy_id:
                        dx = other.x - enemy.x
                        dy = other.y - enemy.y
                        distance = (dx * dx + dy * dy) ** 0.5
                        if distance <= 100:
                            other.hp = min(other.hp + 20, other.max_hp)
        
        # Check if wave should spawn
        if len(game_state.enemies) == 0:
            game_state.spawn_wave()
        
        # Broadcast game state
        state = game_state.get_state()
        await manager.broadcast(json.dumps(state))

@app.on_event("startup")
async def startup_event():
    """Start the game loop when the app starts"""
    asyncio.create_task(game_loop())

@app.get("/")
async def root():
    return {"message": "Tower Defense Backend"}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    logger.info(f"🔌 Client {client_id} attempting to connect")
    await manager.connect(client_id, websocket)
    
    # Add player to game
    player_name = f"Player {len(game_state.players) + 1}"
    game_state.add_player(client_id, player_name)
    logger.info(f"✅ Player added: {player_name} (ID: {client_id})")
    logger.info(f"📊 Total players: {len(game_state.players)}")
    
    # Send initial state
    state = game_state.get_state()
    logger.info(f"📤 Sending initial state to {client_id}: {len(state.get('players', []))} players")
    await websocket.send_text(json.dumps(state))
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            logger.info(f"📨 Received message from {client_id}: {message.get('type')}")
            
            if message["type"] == "place_tower":
                tower_type = message.get("tower_type", "basic")
                x, y = message["x"], message["y"]
                logger.info(f"🏰 {client_id} placing {tower_type} tower at ({x}, {y})")
                
                success = game_state.place_tower(
                    client_id,
                    x,
                    y,
                    tower_type
                )
                
                if success:
                    logger.info(f"✅ Tower placed successfully!")
                else:
                    logger.warning(f"❌ Tower placement failed!")
                    await websocket.send_text(json.dumps({
                        "type": "error",
                        "message": "Cannot place tower there or not enough gold"
                    }))
            
            elif message["type"] == "start_wave":
                logger.info(f"🌊 Starting wave {game_state.wave_number + 1}")
                game_state.spawn_wave()
    
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        logger.info(f"🔌 Client {client_id} disconnected")
    except Exception as e:
        logger.error(f"❌ Error in websocket for {client_id}: {e}")
        manager.disconnect(client_id)

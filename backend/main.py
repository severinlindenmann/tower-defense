from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import logging
from typing import Dict
from models.game import Game

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global game instance
game = Game()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, player_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[player_id] = websocket
        logger.info(f"Player {player_id} connected. Total players: {len(self.active_connections)}")

    def disconnect(self, player_id: str):
        if player_id in self.active_connections:
            del self.active_connections[player_id]
            logger.info(f"Player {player_id} disconnected. Total players: {len(self.active_connections)}")

    async def send_to_player(self, player_id: str, message: dict):
        if player_id in self.active_connections:
            try:
                await self.active_connections[player_id].send_json(message)
            except Exception as e:
                logger.error(f"Error sending to {player_id}: {e}")
                self.disconnect(player_id)

    async def broadcast(self, message: dict):
        """Broadcast message to all connected players"""
        disconnected = []
        for player_id, connection in self.active_connections.items():
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting to {player_id}: {e}")
                disconnected.append(player_id)
        
        for player_id in disconnected:
            self.disconnect(player_id)

manager = ConnectionManager()


@app.get("/")
async def root():
    return {
        "message": "Tower Defense Game API",
        "players": len(game.players),
        "towers": len(game.towers),
        "enemies": len(game.enemies),
        "wave": game.current_wave
    }


@app.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str):
    await manager.connect(player_id, websocket)
    
    # Add player to game
    game.add_player(player_id)
    
    # Send initial game state
    await manager.send_to_player(player_id, {
        "type": "init",
        "state": game.to_dict()
    })
    
    try:
        while True:
            # Receive messages from client
            data = await websocket.receive_text()
            message = json.loads(data)
            
            response = await handle_player_action(player_id, message)
            
            # Broadcast state update to all players
            if response.get("broadcast", True):
                await manager.broadcast({
                    "type": "state_update",
                    "state": game.to_dict(),
                    "events": response.get("events", {})
                })
            else:
                # Send response only to requesting player
                await manager.send_to_player(player_id, response)
    
    except WebSocketDisconnect:
        manager.disconnect(player_id)
        game.remove_player(player_id)
        await manager.broadcast({
            "type": "player_disconnected",
            "player_id": player_id,
            "state": game.to_dict()
        })
    except Exception as e:
        logger.error(f"WebSocket error for {player_id}: {e}")
        manager.disconnect(player_id)
        game.remove_player(player_id)


async def handle_player_action(player_id: str, message: dict) -> dict:
    """Handle player actions"""
    action = message.get("action")
    
    if action == "place_tower":
        result = game.place_tower(
            player_id,
            message.get("x"),
            message.get("y"),
            message.get("tower_type")
        )
        return {
            "type": "tower_placed",
            "result": result,
            "broadcast": result.get("success", False)
        }
    
    elif action == "upgrade_tower":
        result = game.upgrade_tower(
            player_id,
            message.get("tower_id"),
            message.get("upgrade_path", "damage")
        )
        return {
            "type": "tower_upgraded",
            "result": result,
            "broadcast": result.get("success", False)
        }
    
    elif action == "start_wave":
        if not game.game_started:
            game.start_game()
        else:
            game.start_next_wave()
        return {
            "type": "wave_started",
            "result": {"success": True, "wave": game.current_wave},
            "broadcast": True
        }
    
    elif action == "get_state":
        return {
            "type": "state",
            "state": game.to_dict(),
            "broadcast": False
        }
    
    return {
        "type": "error",
        "error": f"Unknown action: {action}",
        "broadcast": False
    }


# Background task for game updates
@app.on_event("startup")
async def startup_event():
    """Start background game loop"""
    asyncio.create_task(game_loop())


async def game_loop():
    """Main game loop that updates game state"""
    logger.info("Game loop started")
    
    while True:
        try:
            # Update game state
            game.update()
            
            # Broadcast updates if game is running
            if game.game_started and manager.active_connections:
                await manager.broadcast({
                    "type": "game_update",
                    "state": game.to_dict()
                })
            
            # Sleep for 100ms (10 ticks per second)
            await asyncio.sleep(0.1)
        
        except Exception as e:
            logger.error(f"Error in game loop: {e}")
            await asyncio.sleep(1)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

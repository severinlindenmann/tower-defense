# 🏰 Tower Defense Game

A multiplayer tower defense game built with React (frontend) and FastAPI (backend) featuring:
- **Object-Oriented Design**: Clean OOP architecture with proper class hierarchies
- **Mobile-First UI**: Responsive, touch-friendly interface
- **Real-Time Multiplayer**: WebSocket-based synchronization
- **Dynamic Terrain**: Randomly generated maps with roads, mountains, and lakes
- **Strategic Gameplay**: 4 tower types, 3 enemy types, terrain bonuses, and upgrade paths

## 🎮 Features

### Towers
- **Basic Tower** (💰100): Balanced stats, works on any terrain
- **Sniper Tower** (💰150): Long range, targets furthest enemy (best on mountains)
- **Cannon Tower** (💰200): High damage, slow attack (best on lakes)
- **AoE Tower** (💰250): Attacks multiple enemies in area

### Terrain Bonuses
- **🏔️ Mountains**: +50% range, -30% damage
- **💧 Lakes**: +50% damage, -40% attack speed
- **🌿 Plains**: Standard stats

### Enemies
- **Fast Enemy** 🔴: Low health, high speed (weak to AoE)
- **Tank Enemy** 🟢: High health, slow speed (weak to Cannon)
- **Flying Enemy** 🟣: Medium stats, resistant to ground towers (weak to Sniper)

### Game Mechanics
- Enemies spawn in waves with increasing difficulty
- Players earn money by defeating enemies
- Place and upgrade towers strategically
- Multiplayer: collaborate with other players
- 20 starting lives (game over when all lives lost)

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn

### Installation & Running

#### Option 1: Use the provided scripts (easiest)

```bash
# Start backend
chmod +x start-backend.sh
./start-backend.sh

# In another terminal, start frontend
chmod +x start-frontend.sh
./start-frontend.sh
```

#### Option 2: Manual setup

**Backend:**
```bash
cd backend
uv sync  # or: pip install -e .
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Access the Game
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🎯 How to Play

1. **Start the Game**: Game auto-starts when first player connects
2. **Select a Tower**: Click on a tower type in the menu (check your money!)
3. **Place Tower**: Click on any non-road cell to place the tower
4. **Upgrade Towers**: Click on existing towers to upgrade damage, range, or speed
5. **Defend**: Towers automatically attack enemies in range
6. **Survive Waves**: Complete waves to earn bonus money and points

### Tips & Strategy
- Place Sniper towers on mountains for maximum range
- Place Cannon towers on lakes for devastating damage
- Use AoE towers near clustered roads
- Upgrade strategically based on enemy types
- Save money for stronger towers in later waves

## 🏗️ Architecture

### Backend (FastAPI + Python OOP)
```
backend/
├── models/
│   ├── tower.py      # Tower classes (Basic, Sniper, Cannon, AoE)
│   ├── enemy.py      # Enemy classes (Fast, Tank, Flying)
│   ├── player.py     # Player class
│   ├── game_map.py   # Map generation with terrain
│   └── game.py       # Main game logic
├── main.py           # FastAPI app with WebSocket
└── pyproject.toml
```

**Key Classes:**
- `Tower`: Base class with terrain bonuses and attack logic
- `Enemy`: Base class with movement, health, and resistances
- `GameMap`: Procedural map generation with A* pathfinding
- `Game`: Game state management, wave system, updates
- `Player`: Track money, points, lives, and stats

### Frontend (React + Canvas)
```
frontend/src/
├── components/
│   ├── GameCanvas.jsx    # Main game rendering
│   ├── TowerMenu.jsx     # Tower selection UI
│   ├── PlayerStats.jsx   # Player info display
│   ├── WaveInfo.jsx      # Wave status
│   └── GameControls.jsx  # Start/restart controls
├── App.jsx              # Main app with WebSocket
└── App.css             # Mobile-first styling
```

**Features:**
- Canvas-based rendering with pixel art style
- Real-time WebSocket updates (10 FPS)
- Touch-friendly UI for mobile devices
- Responsive design (works on desktop and mobile)
- Visual effects for attacks and animations

## 🔧 API Endpoints

### REST API
- `GET /` - API status
- `GET /api/game/state` - Get current game state
- `POST /api/game/start` - Start the game
- `POST /api/towers/place/{player_id}` - Place a tower
- `POST /api/towers/upgrade/{player_id}` - Upgrade a tower

### WebSocket
- `ws://localhost:8000/ws/{player_id}` - Real-time game updates

## 🎨 Customization

### Adjust Game Balance
Edit values in `backend/models/`:
- Tower stats: `tower.py` (damage, range, attack_speed, cost)
- Enemy stats: `enemy.py` (health, speed, resistances, rewards)
- Wave difficulty: `game.py` (`_generate_wave_enemies`)
- Player starting resources: `player.py` (money, lives)

### Modify Map Generation
Edit `backend/models/game_map.py`:
- Grid size: `grid_size` parameter
- Terrain distribution: `_generate_terrain_features`
- Road complexity: `_generate_path` algorithm

### Change Visual Style
Edit `frontend/src/components/GameCanvas.jsx`:
- Colors: `COLORS` constant
- Cell rendering: `drawTerrain`, `drawTowers`, `drawEnemies`
- Animations: `drawAttacks`

## 🐛 Troubleshooting

**Backend won't start:**
- Check Python version: `python --version` (needs 3.10+)
- Install dependencies: `cd backend && uv sync`
- Check port 8000 is available

**Frontend won't connect:**
- Ensure backend is running first
- Check WebSocket URL in `App.jsx` matches backend port
- Clear browser cache and reload

**Game too easy/hard:**
- Adjust starting money in `models/player.py`
- Modify enemy spawn rate in `models/game.py`
- Change tower costs in `models/tower.py`

## 📝 Development Notes

Built from scratch following OOP principles:
- Clean class hierarchies with inheritance
- Factory patterns for tower/enemy creation
- Separation of concerns (models, API, rendering)
- Mobile-first responsive design
- Real-time multiplayer synchronization

## 🤝 Multiplayer

- Multiple players can join the same game session
- All players share the same map and enemies
- Each player has independent money and stats
- Players can place towers anywhere on the map
- Game ends when all players lose all lives
- Collaborative gameplay encouraged!

## 📄 License

This project was created as a demonstration of full-stack game development with OOP principles.

---

**Enjoy defending your tower! 🏰⚔️**

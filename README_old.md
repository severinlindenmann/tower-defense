# Tower Defense Game - Multiplayer 2D Grid-Based

A **multiplayer tower defense game** built with **React** (frontend) and **FastAPI** (backend), featuring a 20x20 grid-based map with terrain effects, tower upgrades, and progressive wave system.

## 🎮 Features

### Game Map
- **20x20 Grid System**: Pixel-art style grid with visual terrain types
- **Dynamic Path Generation**: Random road from one edge to another each game
- **Terrain Types**:
  - **Plains**: Standard terrain with balanced tower stats
  - **Mountains**: Towers get **+50% range** but **-30% damage**
  - **Lakes**: Towers get **+50% damage** but **slower attack speed**

### Towers
- **Basic Tower** (💰 100): Balanced stats, good all-rounder
- **Sniper Tower** (💰 250): Long range, lower damage - excels on mountains
- **Cannon Tower** (💰 300): High damage, slow attack - excels on lakes
- **AoE Tower** (💰 350): Area of effect damage to multiple enemies

#### Tower Upgrade System
Each tower can be upgraded up to 3 levels with three upgrade paths:
- **Damage Path**: +50% damage per level
- **Range Path**: +30% range per level
- **Speed Path**: 20% faster attack speed per level

### Enemies
- **Basic Enemy**: Standard balanced enemy
- **Fast Enemy**: High speed, low health - weak to splash damage
- **Tank Enemy**: High health and armor - weak to cannons, resistant to basic towers
- **Flying Enemy**: Can only be hit by certain towers - weak to snipers
- **Healer Enemy**: Heals nearby enemies
- **Boss Enemy**: Appears every 5 waves with massive health and armor

#### Enemy Abilities
- **Resistances**: Some enemies take reduced damage from certain tower types
- **Weaknesses**: Some enemies take extra damage from specific towers
- **Special Abilities**: Healers can restore health to nearby enemies

### Multiplayer
- Multiple players can join the same game session
- Each player has their own color for tower identification
- Shared map and enemy waves
- Individual gold and scoring system
- Only the player who destroys an enemy gets the reward

### Game Mechanics
- **Progressive Waves**: Enemy count and difficulty increase each wave
- **Economy System**: Earn gold by defeating enemies to build and upgrade towers
- **Lives System**: Each player has 20 lives, lost when enemies reach the end
- **Score Tracking**: Track performance with points earned

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** with `uv` package manager
- **Node.js 16+** with npm

### Installation & Running

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd tower-defense
```

2. **Start Backend** (Terminal 1)
```bash
chmod +x start-backend.sh
./start-backend.sh
```

3. **Start Frontend** (Terminal 2)
```bash
chmod +x start-frontend.sh
./start-frontend.sh
```

4. **Open Game**
- Navigate to `http://localhost:5173`
- Multiple players can connect by opening the same URL in different browsers/tabs

## 🎯 How to Play

### Basic Controls
1. **Select a Tower**: Click on a tower type in the sidebar
2. **Place Tower**: Click on a valid grid cell (plains, mountain, or lake)
3. **Upgrade Tower**: Click on your own tower to see upgrade options
4. **Start Wave**: Click "Spawn Wave" button to begin

### Strategy Tips
- **Mountains** are great for Sniper towers (maximize their range bonus)
- **Lakes** work best for Cannon towers (maximize their damage)
- **Place AoE towers** near path curves where enemies bunch up
- **Upgrade strategically** - range upgrades help cover more area
- **Watch enemy types** - build counters for specific threats
- **Save gold** for boss waves (every 5 waves)

### Terrain Strategy
- **Mountain towers** can cover larger areas but deal less damage - good for support
- **Lake towers** hit harder but slower - place them at critical choke points
- **Plains towers** are versatile - use them for general coverage

## 🏗️ Architecture

### Backend (Python/FastAPI)
```
backend/
├── main.py              # FastAPI server, WebSocket handling, game loop
├── game_state.py        # Main game state management
├── map_generator.py     # 20x20 grid generation with terrain
├── towers.py            # Tower classes with upgrade system
├── enemies.py           # Enemy classes with resistances/weaknesses
├── player.py            # Player state (gold, lives, score)
└── pyproject.toml       # Python dependencies
```

**Key Features:**
- Real-time WebSocket communication
- 10 FPS game loop for enemy movement and tower attacks
- Object-oriented design with tower and enemy class hierarchies
- Terrain-based stat modifiers
- Progressive wave system

### Frontend (React/Vite)
```
frontend/
└── src/
    ├── App.jsx          # Main game component with grid rendering
    ├── App-new.css      # Mobile-first responsive styles
    └── main.jsx         # Entry point
```

**Key Features:**
- Canvas-based grid rendering (20x20 cells)
- Real-time WebSocket updates
- Touch-friendly mobile-first UI
- Tower upgrade interface
- Terrain visualization

## 🎨 UI Design

### Mobile-First
- **Responsive Layout**: Adapts from mobile (single column) to desktop (sidebar + canvas)
- **Touch Controls**: Large tap targets for tower placement
- **Readable Stats**: Clear display of player gold, lives, and score
- **Accessible Buttons**: Easy-to-tap tower selection and upgrade buttons

### Visual Elements
- **Terrain Colors**:
  - Plains: Dark green (`#2d5016`)
  - Mountains: Brown (`#8B7355`) with triangle indicator
  - Lakes: Blue (`#4682B4`) with ripple animation
  - Roads: Brown (`#6b4423`)

- **Tower Colors**: Each tower type has a distinct color
- **Enemy Types**: Different sizes and colors for each enemy type
- **Health Bars**: Visual health display above each enemy

## 🔧 Configuration

### Map Settings
Edit `backend/game_state.py`:
```python
self.map_generator = MapGenerator(grid_size=20)  # Change grid size
```

### Tower Costs
Edit `backend/towers.py` in each tower class:
```python
self.cost = 100  # Adjust tower cost
```

### Wave Difficulty
Edit `backend/enemies.py` in `get_wave_composition()`:
```python
base_count = 5 + wave_number  # Adjust enemy count scaling
```

## 🐛 Troubleshooting

### Backend won't start
- Ensure Python 3.10+ is installed
- Install `uv`: `pip install uv`
- Check port 8000 is not in use

### Frontend won't start
- Ensure Node.js 16+ is installed
- Run `npm install` in `frontend/` directory
- Check port 5173 is not in use

### Connection Issues
- Verify backend is running on `http://localhost:8000`
- Check browser console for WebSocket errors
- Ensure CORS is properly configured in `backend/main.py`

## 🎓 Code Structure (OOP)

### Key Classes

**Tower (Base Class)**
```python
- apply_terrain_bonus(): Modifies stats based on terrain
- upgrade(): Upgrades tower along chosen path
- get_upgrade_cost(): Calculates upgrade cost
```

**Enemy (Base Class)**
```python
- take_damage(): Applies damage with resistances/weaknesses
- Subclasses: BasicEnemy, FastEnemy, TankEnemy, FlyingEnemy, BossEnemy
```

**GameState**
```python
- place_tower(): Validates and places tower with terrain bonuses
- spawn_wave(): Creates enemies with proper path
- upgrade_tower(): Handles tower upgrades
```

**MapGenerator**
```python
- generate_map(): Creates 20x20 grid with terrain
- get_terrain_bonus(): Returns stat modifiers for terrain type
- can_place_tower(): Validates tower placement
```

## 📝 Future Enhancements

- [ ] Add sound effects for tower attacks and enemy deaths
- [ ] Implement tower selling functionality
- [ ] Add more tower types (poison, lightning, etc.)
- [ ] Create boss special abilities
- [ ] Add player chat system
- [ ] Implement game save/load
- [ ] Add achievement system
- [ ] Create multiple map presets
- [ ] Add tower range preview before placement
- [ ] Implement difficulty levels

## 📄 License

MIT License - Feel free to use and modify for your projects!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👨‍💻 Development

### Backend Development
```bash
cd backend
uv pip install -e .
uvicorn main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm run dev
```

### Testing
- Backend: Navigate to `http://localhost:8000/docs` for API documentation
- Frontend: Open browser console to see WebSocket messages

---

**Enjoy defending your base!** 🏰👾

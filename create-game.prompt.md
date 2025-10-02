# Tower Defense Game: React + FastAPI (OOP, Mobile-First)

START FROM SKRETCH, IGNORE ANY DEMO CODE!

## Overview
Generate a **multiplayer tower defense game** for the browser using **React** for the frontend and **FastAPI** for the backend. The game should be built with a **focus on object-oriented programming (OOP)** and **mobile-first design**. The game features a **2D pixel-style grid** (20x20 cells) where players collaborate to defend against waves of enemies by building towers. The map includes a **randomly generated road**, **mountains**, and **lakes**, each affecting tower placement and behavior.

---

## Requirements

### 1. Game Map
- **Grid System**: 20x20 grid with cells for roads, mountains, and lakes.
- **Random Road**: A path from one side of the map to the other, where enemies spawn and move.
- **Terrain Types**:
  - **Mountains**: Towers built here have **long range** but lower damage.
  - **Lakes**: Towers built here have **high damage** but slow attack speed.
  - **Plains**: Standard towers with balanced stats.

### 2. Towers
- **Types**:
  - **Basic Tower**: Low cost, balanced stats.
  - **Sniper Tower**: Long range, low damage (mountains only).
  - **Cannon Tower**: High damage, slow attack speed (lakes only).
  - **AoE Tower**: Attacks multiple enemies in a radius.
- **Upgrades**: Each tower has 2-3 upgrade paths (e.g., damage, range, attack speed).
- **Placement**: Players click a cell and select a tower from a menu.

### 3. Enemies
- **Types**:
  - **Fast Enemy**: Low health, high speed.
  - **Tank Enemy**: High health, slow speed.
  - **Flying Enemy**: Immune to ground towers.
- **Abilities/Weaknesses**: Some enemies are resistant or weak to specific tower types.

### 4. Game Mechanics
- **Wave System**: Enemies spawn in waves, increasing in difficulty over time.
- **Multiplayer**: Players join a game session, share the same map, and collaborate to defend.
- **Economy**:
  - Players earn **money** for defeating enemies.
  - Players earn **points** based on performance.
- **Shop System**: Buy and upgrade towers using earned money.

### 5. Animations & Design
- **Pixel Art Style**: Retro 2D graphics for towers, enemies, and terrain.
- **Animations**:
  - Tower attack animations (e.g., projectiles, explosions).
  - Enemy movement and death animations.
  - Environmental effects (e.g., water ripples on lakes).
- **Mobile-First UI**: Responsive design for touch and desktop.

### 6. Backend (FastAPI)
- **Game Logic**:
  - Handle enemy spawning, movement, and pathfinding.
  - Manage tower attacks, upgrades, and player actions.
- **Multiplayer**:
  - WebSocket or REST API for real-time player interactions.
  - Sync game state (e.g., enemy positions, tower placements) across clients.
- **Data Persistence**: Track player scores, money, and game progress.

### 7. Frontend (React)
- **UI Components**:
  - Grid rendering with terrain and towers.
  - Tower selection menu.
  - Player stats (money, points).
  - Wave timer and enemy health bars.
- **Input Handling**: Touch-friendly controls for mobile.

### 8. Code Structure (OOP)
- **Classes**:
  - `GameMap`: Manages grid, terrain, and pathfinding.
  - `Tower`: Base class with subclasses for each tower type.
  - `Enemy`: Base class with subclasses for each enemy type.
  - `Player`: Tracks money, points, and owned towers.
  - `Game`: Manages game state, waves, and multiplayer logic.
- **State Management**: Use React hooks or a state library (e.g., Redux, Zustand) for frontend state.

### 9. Technical Stack
- **Frontend**: React, TypeScript, Canvas/API for rendering.
- **Backend**: FastAPI, Python, WebSockets (or Socket.IO for real-time).
- **Styling**: CSS Modules or TailwindCSS for responsive design.

### 10. Extras
- **Sound Effects**: Optional but encouraged (e.g., tower attacks, enemy deaths).
- **Local Storage**: Save game progress for single-player mode.

---

## Implementation Notes
- Start from scratch; ignore any existing demo code.
- Use **clean, modular OOP** for maintainability.
- Prioritize **performance** for smooth animations on mobile.
- Include **error handling** for multiplayer sync issues.

---

## Example Code Structure (Suggestions)
```plaintext
frontend/
  ├── components/
  │   ├── GameMap.tsx       # Renders grid and handles cell clicks
  │   ├── TowerMenu.tsx     # Tower selection UI
  │   ├── PlayerStats.tsx   # Displays money/points
  │   └── ...
  ├── hooks/                # Custom hooks for game logic
  ├── assets/               # Pixel art sprites
  └── App.tsx               # Main game component

backend/
  ├── models/
  │   ├── tower.py          # Tower classes
  │   ├── enemy.py          # Enemy classes
  │   └── game.py           # Core game logic
  ├── api/
  │   ├── main.py           # FastAPI routes
  │   └── websocket.py      # Real-time updates
  └── ...

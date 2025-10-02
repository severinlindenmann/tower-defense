# 🎮 Quick Start Guide

## Prerequisites
- Python 3.10+ with `uv` installed
- Node.js 18+ with npm

## Start Playing in 3 Steps:

### 1️⃣ Start the Backend
Open a terminal and run:
```bash
cd /Users/severin/Documents/GitHub/tower-defense
./start-backend.sh
```

You should see:
```
🚀 Starting Backend Server...
INFO: Uvicorn running on http://0.0.0.0:8000
INFO: Game loop started
INFO: Application startup complete.
```

### 2️⃣ Start the Frontend
Open a **new terminal** and run:
```bash
cd /Users/severin/Documents/GitHub/tower-defense
./start-frontend.sh
```

You should see:
```
🚀 Starting Frontend Server...
VITE ready in XXX ms
Local: http://localhost:5173/
```

### 3️⃣ Play the Game
Open your browser and go to:
**http://localhost:5173**

## 🎯 How to Play

1. **Wait for Connection**: The game connects automatically
2. **Select a Tower**: Click on a tower type in the menu (check your money!)
3. **Place Tower**: Click on any green/brown/blue cell (not gray roads!)
4. **Start Wave**: Click "Start Wave" button
5. **Watch & Defend**: Towers automatically attack enemies
6. **Upgrade**: Click on existing towers to upgrade them
7. **Survive**: Complete waves to earn bonus money

## 💡 Strategy Tips

### Tower Placement
- 🏔️ **Mountains (Brown)**: Place Sniper towers (+50% range)
- 💧 **Lakes (Blue)**: Place Cannon towers (+50% damage)
- 🌿 **Plains (Green)**: Basic towers work well

### Enemy Weaknesses
- 🟢 **Fast (Green)**: Weak to AoE towers
- 🔴 **Tank (Red)**: Weak to Cannon towers  
- 🔵 **Flying (Cyan)**: Weak to Sniper towers

### Money Management
- Start with 2-3 Basic towers ($100 each)
- Save $250 for AoE tower at choke points
- Upgrade existing towers before buying new ones
- Each wave completion gives bonus money

## 🎮 Controls

### Desktop
- **Click**: Select tower or place tower
- **Hover**: See tower range
- **Click Tower**: Open upgrade menu

### Mobile/Touch
- **Tap**: Select tower or place tower
- **Tap Tower**: Open upgrade menu
- All buttons are touch-optimized (44px minimum)

## 👥 Multiplayer

- Multiple players can join the same game
- Everyone sees the same map and enemies
- Each player has independent money and stats
- Players can place towers anywhere
- Collaborative defense!

## 🐛 Troubleshooting

**Backend won't start:**
```bash
# Kill any process on port 8000
lsof -ti:8000 | xargs kill -9
# Try again
./start-backend.sh
```

**Frontend won't connect:**
- Make sure backend is running first
- Check http://localhost:8000 shows game info
- Refresh browser page

**Can't place tower:**
- Check you have enough money (top left)
- Can't place on roads (gray cells)
- Can't place where another tower exists

## 📚 More Info

- **Full Documentation**: See `README.md`
- **Implementation Details**: See `IMPLEMENTATION_SUMMARY.md`
- **API Documentation**: http://localhost:8000/docs (when backend running)

## 🎉 Enjoy!

Have fun defending your tower! Try different strategies, experiment with tower combinations, and see how many waves you can survive!

Good luck! 🏰⚔️

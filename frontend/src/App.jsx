import { useState, useEffect, useRef, useCallback } from 'react'
import GameCanvas from './components/GameCanvas'
import TowerMenu from './components/TowerMenu'
import PlayerStats from './components/PlayerStats'
import WaveInfo from './components/WaveInfo'
import './App.css'

function App() {
  const [playerId] = useState(() => Math.random().toString(36).substring(7))
  const [ws, setWs] = useState(null)
  const [gameState, setGameState] = useState(null)
  const [connected, setConnected] = useState(false)
  const [selectedTower, setSelectedTower] = useState('basic')
  const [selectedTowerForUpgrade, setSelectedTowerForUpgrade] = useState(null)
  const [message, setMessage] = useState(null)

  // WebSocket connection
  useEffect(() => {
    console.log('🔌 Connecting to WebSocket with playerId:', playerId)
    const websocket = new WebSocket(`ws://localhost:8000/ws/${playerId}`)
    
    websocket.onopen = () => {
      console.log('✅ Connected to server')
      setConnected(true)
      showMessage('Connected to server', 'success')
    }

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      console.log('📨 Received:', data.type)
      
      if (data.type === 'init' || data.type === 'state_update' || data.type === 'game_update') {
        setGameState(data.state)
        
        // Handle events
        if (data.events) {
          handleGameEvents(data.events)
        }
      } else if (data.type === 'tower_placed') {
        if (data.result.success) {
          showMessage('Tower placed!', 'success')
        } else {
          showMessage(data.result.error, 'error')
        }
      } else if (data.type === 'tower_upgraded') {
        if (data.result.success) {
          showMessage('Tower upgraded!', 'success')
        } else {
          showMessage(data.result.error, 'error')
        }
      } else if (data.type === 'wave_started') {
        if (data.result.success) {
          showMessage(`Wave ${data.result.wave} started!`, 'info')
        }
      }
    }

    websocket.onclose = () => {
      console.log('❌ Disconnected from server')
      setConnected(false)
      showMessage('Disconnected from server', 'error')
    }

    websocket.onerror = (error) => {
      console.error('WebSocket error:', error)
      showMessage('Connection error', 'error')
    }

    setWs(websocket)

    return () => websocket.close()
  }, [playerId])

  const handleGameEvents = (events) => {
    if (events.wave_complete) {
      showMessage('Wave complete! Bonus money earned!', 'success')
    }
    if (events.enemy_deaths && events.enemy_deaths.length > 0) {
      console.log(`💀 ${events.enemy_deaths.length} enemies defeated`)
    }
    if (events.enemy_reached_end && events.enemy_reached_end.length > 0) {
      showMessage(`${events.enemy_reached_end.length} enemies reached the end!`, 'warning')
    }
  }

  const showMessage = (text, type = 'info') => {
    setMessage({ text, type })
    setTimeout(() => setMessage(null), 3000)
  }

  const sendAction = useCallback((action, data = {}) => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ action, ...data }))
    }
  }, [ws])

  const handleCellClick = useCallback((x, y) => {
    if (!gameState) return

    // Check if clicking on existing tower for upgrade
    const tower = Object.values(gameState.towers).find(t => t.x === x && t.y === y)
    if (tower) {
      setSelectedTowerForUpgrade(tower)
      return
    }

    // Place new tower
    if (selectedTower) {
      sendAction('place_tower', {
        x,
        y,
        tower_type: selectedTower
      })
    }
  }, [gameState, selectedTower, sendAction])

  const handleUpgradeTower = useCallback((towerId, upgradePath) => {
    sendAction('upgrade_tower', {
      tower_id: towerId,
      upgrade_path: upgradePath
    })
    setSelectedTowerForUpgrade(null)
  }, [sendAction])

  const handleStartWave = useCallback(() => {
    sendAction('start_wave')
  }, [sendAction])

  const currentPlayer = gameState?.players?.[playerId]

  return (
    <div className="app">
      <div className="app-header">
        <h1>🏰 Tower Defense</h1>
        {!connected && <div className="connection-status">Connecting...</div>}
        {connected && <div className="connection-status connected">●  Connected</div>}
      </div>

      {message && (
        <div className={`message message-${message.type}`}>
          {message.text}
        </div>
      )}

      <div className="game-container">
        <div className="game-main">
          <WaveInfo
            currentWave={gameState?.current_wave || 0}
            waveInProgress={gameState?.wave_in_progress || false}
            enemyCount={Object.keys(gameState?.enemies || {}).length}
            onStartWave={handleStartWave}
          />

          <GameCanvas
            gameState={gameState}
            onCellClick={handleCellClick}
            selectedTower={selectedTower}
          />

          <PlayerStats player={currentPlayer} />
        </div>

        <div className="game-sidebar">
          <TowerMenu
            selectedTower={selectedTower}
            onSelectTower={setSelectedTower}
            playerMoney={currentPlayer?.money || 0}
          />

          {selectedTowerForUpgrade && (
            <div className="upgrade-panel">
              <h3>Upgrade Tower</h3>
              <div className="tower-info">
                <p><strong>Type:</strong> {selectedTowerForUpgrade.type}</p>
                <p><strong>Level:</strong> {selectedTowerForUpgrade.level}</p>
                <p><strong>Damage:</strong> {selectedTowerForUpgrade.damage.toFixed(1)}</p>
                <p><strong>Range:</strong> {selectedTowerForUpgrade.range.toFixed(1)}</p>
                <p><strong>Speed:</strong> {selectedTowerForUpgrade.attack_speed.toFixed(2)}/s</p>
              </div>
              <div className="upgrade-buttons">
                <button
                  onClick={() => handleUpgradeTower(selectedTowerForUpgrade.id, 'damage')}
                  disabled={selectedTowerForUpgrade.level >= 5}
                >
                  ⚔️ Damage
                </button>
                <button
                  onClick={() => handleUpgradeTower(selectedTowerForUpgrade.id, 'range')}
                  disabled={selectedTowerForUpgrade.level >= 5}
                >
                  🎯 Range
                </button>
                <button
                  onClick={() => handleUpgradeTower(selectedTowerForUpgrade.id, 'speed')}
                  disabled={selectedTowerForUpgrade.level >= 5}
                >
                  ⚡ Speed
                </button>
              </div>
              <button
                className="close-button"
                onClick={() => setSelectedTowerForUpgrade(null)}
              >
                Close
              </button>
            </div>
          )}
        </div>
      </div>

      {gameState?.game_over && (
        <div className="game-over-overlay">
          <div className="game-over-panel">
            <h2>Game Over!</h2>
            <p>Wave: {gameState.current_wave}</p>
            <p>Score: {currentPlayer?.points || 0}</p>
            <button onClick={() => window.location.reload()}>Play Again</button>
          </div>
        </div>
      )}
    </div>
  )
}

export default App

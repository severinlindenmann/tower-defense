import { useState, useEffect, useRef } from 'react'
import './App-mobile.css'

function App() {
  const [playerId] = useState(() => Math.random().toString(36).substring(7))
  const [ws, setWs] = useState(null)
  const [gameState, setGameState] = useState(null)
  const [connected, setConnected] = useState(false)
  const [selectedTower, setSelectedTower] = useState('basic')
  const [particles, setParticles] = useState([])
  const canvasRef = useRef(null)
  const animationRef = useRef(null)
  const lastFireTime = useRef({})

  // WebSocket connection
  useEffect(() => {
    console.log('🔌 Connecting to WebSocket with playerId:', playerId)
    const websocket = new WebSocket(`ws://localhost:8000/ws/${playerId}`)
    
    websocket.onopen = () => {
      console.log('✅ Connected to server')
      setConnected(true)
    }

    websocket.onmessage = (event) => {
      const message = JSON.parse(event.data)
      console.log('📨 Received message:', message)
      
      // The backend sends the state directly, not nested in game_state
      if (message.players !== undefined) {
        console.log('📊 Setting game state. Players:', Object.keys(message.players || {}).length)
        setGameState(message)
      }
      
      // Show particles on enemy destroyed
      if (message.type === 'enemy_destroyed') {
        const enemy = gameState?.enemies?.find(e => e.id === message.enemy_id)
        if (enemy) {
          createExplosion(enemy.x, enemy.y)
        }
      }
    }

    websocket.onclose = () => {
      console.log('❌ Disconnected from server')
      setConnected(false)
    }

    websocket.onerror = (error) => {
      console.error('⚠️ WebSocket error:', error)
    }

    setWs(websocket)

    return () => {
      console.log('🔌 Closing WebSocket connection')
      websocket.close()
    }
  }, [playerId])

  const createExplosion = (x, y) => {
    const newParticles = []
    for (let i = 0; i < 20; i++) {
      newParticles.push({
        x,
        y,
        vx: (Math.random() - 0.5) * 8,
        vy: (Math.random() - 0.5) * 8 - 2,
        life: 60,
        maxLife: 60,
        color: `hsl(${Math.random() * 60 + 10}, 100%, 50%)`,
        size: Math.random() * 4 + 2
      })
    }
    setParticles(prev => [...prev, ...newParticles])
  }

  // Game rendering with smooth animations
  useEffect(() => {
    if (!gameState || !canvasRef.current) return

    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    const now = Date.now()

    const render = () => {
      // Clear canvas with gradient background
      const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height)
      gradient.addColorStop(0, '#1a472a')
      gradient.addColorStop(1, '#2d5016')
      ctx.fillStyle = gradient
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      // Draw decorative grass pattern
      ctx.fillStyle = 'rgba(0, 100, 0, 0.1)'
      for (let i = 0; i < canvas.width; i += 40) {
        for (let j = 0; j < canvas.height; j += 40) {
          if (Math.random() > 0.5) {
            ctx.fillRect(i, j, 2, 2)
          }
        }
      }

      // Draw path with shadow and texture
      ctx.shadowBlur = 15
      ctx.shadowColor = 'rgba(0, 0, 0, 0.5)'
      ctx.fillStyle = '#6b4423'
      ctx.fillRect(0, 220, canvas.width, 60)
      
      // Path edges
      ctx.strokeStyle = '#4a2f1a'
      ctx.lineWidth = 3
      ctx.beginPath()
      ctx.moveTo(0, 220)
      ctx.lineTo(canvas.width, 220)
      ctx.stroke()
      ctx.beginPath()
      ctx.moveTo(0, 280)
      ctx.lineTo(canvas.width, 280)
      ctx.stroke()
      
      ctx.shadowBlur = 0

      // Draw towers with player colors and animations
      gameState.towers?.forEach(tower => {
        const pulse = Math.sin(Date.now() / 500) * 0.2 + 1
        
        // Tower shadow
        ctx.fillStyle = 'rgba(0, 0, 0, 0.3)'
        ctx.beginPath()
        ctx.ellipse(tower.x + 2, tower.y + 18, 12, 4, 0, 0, Math.PI * 2)
        ctx.fill()
        
        // Range indicator (subtle)
        ctx.strokeStyle = `${tower.owner_color}33`
        ctx.lineWidth = 2
        ctx.beginPath()
        ctx.arc(tower.x, tower.y, tower.range, 0, Math.PI * 2)
        ctx.stroke()
        
        // Tower base with owner color
        const baseColor = tower.owner_color || '#888'
        ctx.fillStyle = baseColor
        ctx.beginPath()
        ctx.arc(tower.x, tower.y, 18, 0, Math.PI * 2)
        ctx.fill()
        
        // Tower type indicator
        let typeColor
        if (tower.type === 'basic') typeColor = '#4169E1'  // Royal Blue
        else if (tower.type === 'fast') typeColor = '#FFD700'  // Gold
        else if (tower.type === 'heavy') typeColor = '#DC143C'  // Crimson
        else if (tower.type === 'sniper') typeColor = '#9370DB'  // Medium Purple
        else if (tower.type === 'splash') typeColor = '#FF8C00'  // Dark Orange
        else if (tower.type === 'freeze') typeColor = '#00CED1'  // Dark Turquoise
        else typeColor = '#888'
        
        ctx.fillStyle = typeColor
        ctx.beginPath()
        ctx.arc(tower.x, tower.y, 12 * pulse, 0, Math.PI * 2)
        ctx.fill()
        
        // Tower highlight
        ctx.fillStyle = 'rgba(255, 255, 255, 0.3)'
        ctx.beginPath()
        ctx.arc(tower.x - 4, tower.y - 4, 5, 0, Math.PI * 2)
        ctx.fill()
        
        // Tower border
        ctx.strokeStyle = '#000'
        ctx.lineWidth = 2
        ctx.beginPath()
        ctx.arc(tower.x, tower.y, 12, 0, Math.PI * 2)
        ctx.stroke()
      })

      // Update and draw particles
      setParticles(prev => {
        const updated = prev.map(p => ({
          ...p,
          x: p.x + p.vx,
          y: p.y + p.vy,
          vy: p.vy + 0.2, // gravity
          life: p.life - 1
        })).filter(p => p.life > 0)
        
        return updated
      })

      particles.forEach(p => {
        const alpha = p.life / p.maxLife
        ctx.fillStyle = p.color.replace(')', `, ${alpha})`)
        ctx.beginPath()
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2)
        ctx.fill()
      })

      // Draw enemies with smooth movement and better graphics
      gameState.enemies?.forEach(enemy => {
        // Smooth enemy movement
        if (!enemy.currentX) enemy.currentX = enemy.x
        if (!enemy.currentY) enemy.currentY = enemy.y
        
        enemy.currentX += (enemy.x - enemy.currentX) * 0.3
        enemy.currentY += (enemy.y - enemy.currentY) * 0.3
        
        // Update enemy position
        enemy.x += enemy.speed || 1
        
        const x = enemy.currentX
        const y = enemy.currentY
        
        // Determine enemy size and colors based on type
        let enemySize = 12
        let enemyColor1 = '#FF4444'
        let enemyColor2 = '#CC0000'
        
        if (enemy.type === 'runner') {
          enemySize = 9
          enemyColor1 = '#FFFF00'  // Yellow
          enemyColor2 = '#FFA500'  // Orange
        } else if (enemy.type === 'tank') {
          enemySize = 16
          enemyColor1 = '#808080'  // Gray
          enemyColor2 = '#404040'  // Dark Gray
        } else if (enemy.type === 'flying') {
          enemySize = 10
          enemyColor1 = '#87CEEB'  // Sky Blue
          enemyColor2 = '#4682B4'  // Steel Blue
        } else if (enemy.type === 'boss') {
          enemySize = 20
          enemyColor1 = '#800080'  // Purple
          enemyColor2 = '#4B0082'  // Indigo
        } else if (enemy.type === 'healer') {
          enemySize = 11
          enemyColor1 = '#90EE90'  // Light Green
          enemyColor2 = '#228B22'  // Forest Green
        }
        
        // Enemy shadow
        ctx.fillStyle = 'rgba(0, 0, 0, 0.3)'
        ctx.beginPath()
        ctx.ellipse(x, y + 15, enemySize * 0.7, 3, 0, 0, Math.PI * 2)
        ctx.fill()
        
        // Enemy body with gradient
        const enemyGradient = ctx.createRadialGradient(x, y, 0, x, y, enemySize)
        enemyGradient.addColorStop(0, enemyColor1)
        enemyGradient.addColorStop(1, enemyColor2)
        ctx.fillStyle = enemyGradient
        ctx.beginPath()
        ctx.arc(x, y, enemySize, 0, Math.PI * 2)
        ctx.fill()
        
        // Flying enemy wings
        if (enemy.type === 'flying') {
          const wingOffset = Math.sin(Date.now() / 100) * 3
          ctx.fillStyle = 'rgba(135, 206, 235, 0.5)'
          ctx.beginPath()
          ctx.ellipse(x - 8, y + wingOffset, 8, 4, 0, 0, Math.PI * 2)
          ctx.fill()
          ctx.beginPath()
          ctx.ellipse(x + 8, y + wingOffset, 8, 4, 0, 0, Math.PI * 2)
          ctx.fill()
        }
        
        // Boss crown
        if (enemy.type === 'boss') {
          ctx.fillStyle = '#FFD700'
          ctx.beginPath()
          ctx.moveTo(x - 8, y - 18)
          ctx.lineTo(x - 4, y - 14)
          ctx.lineTo(x, y - 18)
          ctx.lineTo(x + 4, y - 14)
          ctx.lineTo(x + 8, y - 18)
          ctx.lineTo(x + 6, y - 12)
          ctx.lineTo(x - 6, y - 12)
          ctx.fill()
        }
        
        // Healer cross
        if (enemy.type === 'healer') {
          ctx.fillStyle = '#FFFFFF'
          ctx.fillRect(x - 1, y - 6, 2, 12)
          ctx.fillRect(x - 6, y - 1, 12, 2)
        }
        
        // Enemy eyes
        const eyeSize = enemySize * 0.25
        ctx.fillStyle = '#FFF'
        ctx.beginPath()
        ctx.arc(x - enemySize * 0.3, y - 2, eyeSize, 0, Math.PI * 2)
        ctx.fill()
        ctx.beginPath()
        ctx.arc(x + enemySize * 0.3, y - 2, eyeSize, 0, Math.PI * 2)
        ctx.fill()
        
        ctx.fillStyle = '#000'
        ctx.beginPath()
        ctx.arc(x - enemySize * 0.25, y - 2, eyeSize * 0.7, 0, Math.PI * 2)
        ctx.fill()
        ctx.beginPath()
        ctx.arc(x + enemySize * 0.35, y - 2, eyeSize * 0.7, 0, Math.PI * 2)
        ctx.fill()
        
        // Enemy border
        ctx.strokeStyle = '#000'
        ctx.lineWidth = 2
        ctx.beginPath()
        ctx.arc(x, y, enemySize, 0, Math.PI * 2)
        ctx.stroke()
        
        // Health bar background
        const barWidth = enemySize * 3
        ctx.fillStyle = 'rgba(0, 0, 0, 0.5)'
        ctx.fillRect(x - barWidth/2, y - enemySize - 12, barWidth, 6)
        
        // Health bar
        const healthPercent = enemy.health / (enemy.max_health || 100)
        const healthColor = healthPercent > 0.5 ? '#00FF00' : 
                           healthPercent > 0.25 ? '#FFFF00' : '#FF0000'
        ctx.fillStyle = healthColor
        ctx.fillRect(x - barWidth/2 + 1, y - enemySize - 11, (barWidth - 2) * healthPercent, 4)
        
        // Health bar border
        ctx.strokeStyle = '#FFF'
        ctx.lineWidth = 1
        ctx.strokeRect(x - barWidth/2, y - enemySize - 12, barWidth, 6)
      })

      // Check for enemies reaching the end
      gameState.enemies?.forEach(enemy => {
        if (enemy.x > 820 && ws) {
          ws.send(JSON.stringify({
            type: 'enemy_reached_end',
            enemy_id: enemy.id
          }))
        }
      })

      // Tower attack logic with visual effects
      gameState.towers?.forEach(tower => {
        const towerId = tower.id
        const lastFire = lastFireTime.current[towerId] || 0
        const fireDelay = 1000 / (tower.fire_rate || 0.3)
        
        if (now - lastFire < fireDelay) return
        
        // Find closest enemy in range
        let targetEnemy = null
        let minDistance = Infinity
        
        gameState.enemies?.forEach(enemy => {
          const dx = (enemy.currentX || enemy.x) - tower.x
          const dy = (enemy.currentY || enemy.y) - tower.y
          const distance = Math.sqrt(dx * dx + dy * dy)
          
          if (distance < tower.range && enemy.health > 0 && distance < minDistance) {
            minDistance = distance
            targetEnemy = enemy
          }
        })
        
        if (targetEnemy) {
          // Draw attack beam with glow
          const gradient = ctx.createLinearGradient(
            tower.x, tower.y,
            targetEnemy.currentX || targetEnemy.x, targetEnemy.currentY || targetEnemy.y
          )
          gradient.addColorStop(0, tower.owner_color || '#FFFF00')
          gradient.addColorStop(1, 'rgba(255, 255, 0, 0)')
          
          ctx.shadowBlur = 10
          ctx.shadowColor = tower.owner_color || '#FFFF00'
          ctx.strokeStyle = gradient
          ctx.lineWidth = 3
          ctx.beginPath()
          ctx.moveTo(tower.x, tower.y)
          ctx.lineTo(targetEnemy.currentX || targetEnemy.x, targetEnemy.currentY || targetEnemy.y)
          ctx.stroke()
          ctx.shadowBlur = 0
          
          // Damage enemy
          const damage = (tower.damage || 10) * 0.016 // Normalize for frame rate
          targetEnemy.health -= damage
          
          if (targetEnemy.health <= 0 && ws) {
            ws.send(JSON.stringify({
              type: 'enemy_destroyed',
              enemy_id: targetEnemy.id,
              tower_owner_id: tower.owner
            }))
          }
          
          lastFireTime.current[towerId] = now
        }
      })

      animationRef.current = requestAnimationFrame(render)
    }

    render()

    return () => {
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current)
      }
    }
  }, [gameState, ws, particles])

  const handleCanvasClick = (e) => {
    if (!ws || !connected) return

    const rect = canvasRef.current.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top

    // Don't allow placing towers on the path
    if (y > 220 && y < 280) {
      return
    }

    ws.send(JSON.stringify({
      type: 'place_tower',
      x: Math.round(x),
      y: Math.round(y),
      tower_type: selectedTower
    }))
  }

  const startGame = () => {
    if (ws && connected) {
      ws.send(JSON.stringify({ type: 'start_game' }))
    }
  }

  const spawnWave = () => {
    if (ws && connected) {
      ws.send(JSON.stringify({ type: 'spawn_wave' }))
    }
  }

  const currentPlayer = gameState?.players?.[playerId]

  return (
    <div className="app">
      <header className="header">
        <h1>🏰 Multiplayer Tower Defense</h1>
        <div className="connection-status">
          {connected ? '🟢 Connected' : '🔴 Disconnected'}
        </div>
      </header>

      <div className="game-container">
        <aside className="sidebar">
          <div className="player-info" style={{ borderColor: currentPlayer?.color }}>
            <h2>Your Stats</h2>
            {currentPlayer && (
              <>
                <div className="stat-item">
                  <span className="stat-icon">💰</span>
                  <span className="stat-label">Gold:</span>
                  <span className="stat-value">{currentPlayer.gold}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-icon">❤️</span>
                  <span className="stat-label">Lives:</span>
                  <span className="stat-value">{currentPlayer.lives}</span>
                </div>
                <div className="stat-item">
                  <span className="stat-icon">⭐</span>
                  <span className="stat-label">Score:</span>
                  <span className="stat-value">{currentPlayer.score}</span>
                </div>
                <div className="player-color-indicator">
                  <span>Your color: </span>
                  <div 
                    className="color-box"
                    style={{ backgroundColor: currentPlayer.color }}
                  ></div>
                </div>
              </>
            )}
          </div>

          <div className="tower-selection">
            <h3>🏰 Select Tower</h3>
            <div className="tower-grid">
              <button 
                className={`tower-btn ${selectedTower === 'basic' ? 'selected' : ''}`}
                onClick={() => setSelectedTower('basic')}
              >
                <span className="tower-icon">🔵</span>
                <div className="tower-info">
                  <div className="tower-name">Basic</div>
                  <div className="tower-cost">💰 100</div>
                  <div className="tower-stats">Balanced</div>
                </div>
              </button>
              <button 
                className={`tower-btn ${selectedTower === 'fast' ? 'selected' : ''}`}
                onClick={() => setSelectedTower('fast')}
              >
                <span className="tower-icon">🟡</span>
                <div className="tower-info">
                  <div className="tower-name">Fast</div>
                  <div className="tower-cost">💰 150</div>
                  <div className="tower-stats">Rapid Fire</div>
                </div>
              </button>
              <button 
                className={`tower-btn ${selectedTower === 'heavy' ? 'selected' : ''}`}
                onClick={() => setSelectedTower('heavy')}
              >
                <span className="tower-icon">🔴</span>
                <div className="tower-info">
                  <div className="tower-name">Heavy</div>
                  <div className="tower-cost">💰 200</div>
                  <div className="tower-stats">High DMG</div>
                </div>
              </button>
              <button 
                className={`tower-btn ${selectedTower === 'sniper' ? 'selected' : ''}`}
                onClick={() => setSelectedTower('sniper')}
              >
                <span className="tower-icon">🎯</span>
                <div className="tower-info">
                  <div className="tower-name">Sniper</div>
                  <div className="tower-cost">💰 300</div>
                  <div className="tower-stats">Long Range</div>
                </div>
              </button>
              <button 
                className={`tower-btn ${selectedTower === 'splash' ? 'selected' : ''}`}
                onClick={() => setSelectedTower('splash')}
              >
                <span className="tower-icon">💥</span>
                <div className="tower-info">
                  <div className="tower-name">Splash</div>
                  <div className="tower-cost">💰 250</div>
                  <div className="tower-stats">Area DMG</div>
                </div>
              </button>
              <button 
                className={`tower-btn ${selectedTower === 'freeze' ? 'selected' : ''}`}
                onClick={() => setSelectedTower('freeze')}
              >
                <span className="tower-icon">❄️</span>
                <div className="tower-info">
                  <div className="tower-name">Freeze</div>
                  <div className="tower-cost">💰 200</div>
                  <div className="tower-stats">Slows</div>
                </div>
              </button>
            </div>
          </div>

          <div className="game-controls">
            <h3>⚙️ Controls</h3>
            <button 
              className="control-btn start-btn"
              onClick={startGame} 
              disabled={!connected || gameState?.game_started}
            >
              🎮 Start Game
            </button>
            <button 
              className="control-btn wave-btn"
              onClick={spawnWave} 
              disabled={!connected || !gameState?.game_started}
            >
              🌊 Spawn Wave {gameState?.wave_number ? `(${gameState.wave_number + 1})` : '(1)'}
            </button>
          </div>

          <div className="players-list">
            <h3>Players ({Object.keys(gameState?.players || {}).length})</h3>
            {Object.values(gameState?.players || {}).map(player => (
              <div 
                key={player.id} 
                className="player-item"
                style={{ borderLeftColor: player.color }}
              >
                <div className="player-header">
                  <div 
                    className="player-color-dot"
                    style={{ backgroundColor: player.color }}
                  ></div>
                  <strong>{player.name}</strong>
                  {player.id === playerId && <span className="you-badge">YOU</span>}
                </div>
                <div className="player-stats">
                  <span>💰 {player.gold}</span>
                  <span>❤️ {player.lives}</span>
                  <span>⭐ {player.score}</span>
                </div>
              </div>
            ))}
          </div>
        </aside>

        <main className="game-area">
          <canvas
            ref={canvasRef}
            width={800}
            height={500}
            onClick={handleCanvasClick}
            className="game-canvas"
          />
          <div className="game-info">
            <div className="info-item">
              <span className="info-label">Click to place towers!</span>
              <span className="info-hint">(Avoid the brown path)</span>
            </div>
            <div className="info-stats">
              <span>👹 Enemies: {gameState?.enemies?.length || 0}</span>
              <span>🗼 Towers: {gameState?.towers?.length || 0}</span>
              <span>🌊 Wave: {gameState?.wave_number || 0}</span>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

export default App

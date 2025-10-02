import { useEffect, useRef, useState } from 'react'
import PropTypes from 'prop-types'

const COLORS = {
  plains: '#90EE90',
  mountain: '#8B7355',
  lake: '#4169E1',
  road: '#696969',
  roadBorder: '#555555',
  grid: '#00000020',
  towerBasic: '#FF6B6B',
  towerSniper: '#4ECDC4',
  towerCannon: '#FFE66D',
  towerAoe: '#A78BFA',
  enemyFast: '#FF4444',
  enemyTank: '#00AA00',
  enemyFlying: '#8844FF',
  healthBar: '#FF0000',
  healthBarBg: '#333333',
  rangeIndicator: '#FFFF0050',
  selected: '#FFFF0080'
}

function GameCanvas({ gameState, onCellClick, selectedTower, selectedTowerForUpgrade }) {
  const canvasRef = useRef(null)
  const [hoveredCell, setHoveredCell] = useState(null)
  const [canvasSize, setCanvasSize] = useState({ width: 600, height: 600 })
  const animationFrameRef = useRef(null)

  // Calculate canvas size based on window
  useEffect(() => {
    const updateSize = () => {
      const maxWidth = Math.min(window.innerWidth - 400, 800)
      const maxHeight = Math.min(window.innerHeight - 200, 800)
      const size = Math.min(maxWidth, maxHeight)
      setCanvasSize({ width: size, height: size })
    }

    updateSize()
    window.addEventListener('resize', updateSize)
    return () => window.removeEventListener('resize', updateSize)
  }, [])

  // Main render function
  useEffect(() => {
    if (!gameState || !gameState.game_map || !canvasRef.current) return

    const canvas = canvasRef.current
    const ctx = canvas.getContext('2d')
    const map = gameState.game_map
    const gridSize = map.grid_size
    const cellSize = canvasSize.width / gridSize

    const render = () => {
      // Clear canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height)

      // Draw terrain
      drawTerrain(ctx, map, cellSize, gridSize)

      // Draw grid
      drawGrid(ctx, cellSize, gridSize)

      // Draw range indicator for hovered cell or selected tower
      if (hoveredCell) {
        drawRangeIndicator(ctx, hoveredCell.x, hoveredCell.y, cellSize, selectedTower)
      }
      if (selectedTowerForUpgrade) {
        drawRangeIndicator(ctx, selectedTowerForUpgrade.x, selectedTowerForUpgrade.y, 
                          cellSize, null, selectedTowerForUpgrade.range)
      }

      // Draw towers
      drawTowers(ctx, gameState.towers, cellSize, selectedTowerForUpgrade)

      // Draw enemies
      drawEnemies(ctx, gameState.enemies, cellSize)

      // Draw attacks
      if (gameState.recent_attacks) {
        drawAttacks(ctx, gameState.recent_attacks, cellSize)
      }

      // Draw hover highlight
      if (hoveredCell) {
        drawHoverHighlight(ctx, hoveredCell.x, hoveredCell.y, cellSize)
      }

      animationFrameRef.current = requestAnimationFrame(render)
    }

    render()

    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
      }
    }
  }, [gameState, hoveredCell, selectedTower, selectedTowerForUpgrade, canvasSize])

  const drawTerrain = (ctx, map, cellSize, gridSize) => {
    for (let y = 0; y < gridSize; y++) {
      for (let x = 0; x < gridSize; x++) {
        const terrain = map.terrain[y][x]
        ctx.fillStyle = COLORS[terrain] || COLORS.plains

        ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize)

        // Add texture to mountains
        if (terrain === 'mountain') {
          ctx.fillStyle = '#00000020'
          ctx.fillRect(x * cellSize + cellSize * 0.2, y * cellSize + cellSize * 0.2, 
                      cellSize * 0.3, cellSize * 0.3)
        }

        // Add ripple effect to lakes
        if (terrain === 'lake') {
          ctx.strokeStyle = '#00000030'
          ctx.lineWidth = 1
          ctx.beginPath()
          ctx.arc(x * cellSize + cellSize / 2, y * cellSize + cellSize / 2, 
                 cellSize * 0.3, 0, Math.PI * 2)
          ctx.stroke()
        }
      }
    }
  }

  const drawGrid = (ctx, cellSize, gridSize) => {
    ctx.strokeStyle = COLORS.grid
    ctx.lineWidth = 1

    for (let i = 0; i <= gridSize; i++) {
      ctx.beginPath()
      ctx.moveTo(i * cellSize, 0)
      ctx.lineTo(i * cellSize, gridSize * cellSize)
      ctx.stroke()

      ctx.beginPath()
      ctx.moveTo(0, i * cellSize)
      ctx.lineTo(gridSize * cellSize, i * cellSize)
      ctx.stroke()
    }
  }

  const drawRangeIndicator = (ctx, x, y, cellSize, towerType, range = null) => {
    if (range === null) {
      // Estimate range based on tower type
      const ranges = { basic: 3, sniper: 5, cannon: 2.5, aoe: 2.5 }
      range = ranges[towerType] || 3
    }

    ctx.fillStyle = COLORS.rangeIndicator
    ctx.beginPath()
    ctx.arc((x + 0.5) * cellSize, (y + 0.5) * cellSize, range * cellSize, 0, Math.PI * 2)
    ctx.fill()
  }

  const drawHoverHighlight = (ctx, x, y, cellSize) => {
    ctx.strokeStyle = COLORS.selected
    ctx.lineWidth = 3
    ctx.strokeRect(x * cellSize + 2, y * cellSize + 2, cellSize - 4, cellSize - 4)
  }

  const drawTowers = (ctx, towers, cellSize, selectedTower) => {
    if (!towers) return

    Object.values(towers).forEach(tower => {
      const centerX = (tower.x + 0.5) * cellSize
      const centerY = (tower.y + 0.5) * cellSize
      const size = cellSize * 0.6

      // Tower color based on type
      const colorMap = {
        basic: COLORS.towerBasic,
        sniper: COLORS.towerSniper,
        cannon: COLORS.towerCannon,
        aoe: COLORS.towerAoe
      }
      ctx.fillStyle = colorMap[tower.type] || COLORS.towerBasic

      // Draw tower base
      ctx.fillRect(centerX - size / 2, centerY - size / 2, size, size)

      // Draw tower top (darker)
      ctx.fillStyle = '#00000040'
      ctx.fillRect(centerX - size / 3, centerY - size / 3, size * 0.66, size * 0.66)

      // Draw level indicator
      ctx.fillStyle = '#FFFFFF'
      ctx.font = `${cellSize * 0.3}px monospace`
      ctx.textAlign = 'center'
      ctx.textBaseline = 'middle'
      ctx.fillText(tower.level, centerX, centerY)

      // Highlight if selected
      if (selectedTower && selectedTower.id === tower.id) {
        ctx.strokeStyle = '#FFFF00'
        ctx.lineWidth = 2
        ctx.strokeRect(centerX - size / 2 - 2, centerY - size / 2 - 2, size + 4, size + 4)
      }
    })
  }

  const drawEnemies = (ctx, enemies, cellSize) => {
    if (!enemies) return

    Object.values(enemies).forEach(enemy => {
      if (!enemy.is_alive) return

      const centerX = (enemy.x + 0.5) * cellSize
      const centerY = (enemy.y + 0.5) * cellSize
      const size = cellSize * 0.5

      // Enemy color based on type
      const colorMap = {
        fast: COLORS.enemyFast,
        tank: COLORS.enemyTank,
        flying: COLORS.enemyFlying
      }
      ctx.fillStyle = colorMap[enemy.type] || COLORS.enemyFast

      // Draw enemy (circle)
      ctx.beginPath()
      ctx.arc(centerX, centerY, size / 2, 0, Math.PI * 2)
      ctx.fill()

      // Draw health bar
      const barWidth = cellSize * 0.6
      const barHeight = cellSize * 0.1
      const barX = centerX - barWidth / 2
      const barY = centerY - size / 2 - barHeight - 2

      // Background
      ctx.fillStyle = COLORS.healthBarBg
      ctx.fillRect(barX, barY, barWidth, barHeight)

      // Health
      ctx.fillStyle = COLORS.healthBar
      const healthWidth = barWidth * enemy.health_percentage
      ctx.fillRect(barX, barY, healthWidth, barHeight)
    })
  }

  const drawAttacks = (ctx, attacks, cellSize) => {
    attacks.forEach(attack => {
      if (attack.type === 'aoe' && attack.targets) {
        // Draw AoE explosion
        attack.targets.forEach(target => {
          const x = (target.x + 0.5) * cellSize
          const y = (target.y + 0.5) * cellSize
          
          ctx.fillStyle = '#FFA50060'
          ctx.beginPath()
          ctx.arc(x, y, (attack.radius || 1.5) * cellSize, 0, Math.PI * 2)
          ctx.fill()
        })
      } else if (attack.target) {
        // Draw projectile line
        const tower = Object.values(gameState.towers || {}).find(t => t.id === attack.tower_id)
        if (tower) {
          ctx.strokeStyle = '#FFFF0080'
          ctx.lineWidth = 2
          ctx.beginPath()
          ctx.moveTo((tower.x + 0.5) * cellSize, (tower.y + 0.5) * cellSize)
          ctx.lineTo((attack.target.x + 0.5) * cellSize, (attack.target.y + 0.5) * cellSize)
          ctx.stroke()
        }
      }
    })
  }

  const handleCanvasClick = (e) => {
    const canvas = canvasRef.current
    const rect = canvas.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top
    
    const cellSize = canvasSize.width / gameState.game_map.grid_size
    const cellX = Math.floor(x / cellSize)
    const cellY = Math.floor(y / cellSize)

    if (cellX >= 0 && cellX < gameState.game_map.grid_size && 
        cellY >= 0 && cellY < gameState.game_map.grid_size) {
      onCellClick(cellX, cellY)
    }
  }

  const handleCanvasMouseMove = (e) => {
    const canvas = canvasRef.current
    const rect = canvas.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top
    
    const cellSize = canvasSize.width / gameState.game_map.grid_size
    const cellX = Math.floor(x / cellSize)
    const cellY = Math.floor(y / cellSize)

    if (cellX >= 0 && cellX < gameState.game_map.grid_size && 
        cellY >= 0 && cellY < gameState.game_map.grid_size) {
      setHoveredCell({ x: cellX, y: cellY })
    } else {
      setHoveredCell(null)
    }
  }

  const handleCanvasMouseLeave = () => {
    setHoveredCell(null)
  }

  return (
    <canvas
      ref={canvasRef}
      width={canvasSize.width}
      height={canvasSize.height}
      onClick={handleCanvasClick}
      onMouseMove={handleCanvasMouseMove}
      onMouseLeave={handleCanvasMouseLeave}
      style={{ 
        border: '3px solid #333',
        borderRadius: '8px',
        cursor: 'pointer',
        touchAction: 'none'
      }}
    />
  )
}

GameCanvas.propTypes = {
  gameState: PropTypes.object.isRequired,
  onCellClick: PropTypes.func.isRequired,
  selectedTower: PropTypes.string,
  selectedTowerForUpgrade: PropTypes.object
}

export default GameCanvas

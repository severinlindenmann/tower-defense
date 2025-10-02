import PropTypes from 'prop-types'
import './TowerMenu.css'

const TOWER_INFO = {
  basic: {
    name: 'Basic Tower',
    cost: 100,
    description: 'Balanced stats, works on any terrain',
    damage: 10,
    range: 3,
    speed: 1.0,
    icon: '🔴'
  },
  sniper: {
    name: 'Sniper Tower',
    cost: 150,
    description: 'Long range, targets furthest enemy. Best on mountains',
    damage: 8,
    range: 5,
    speed: 0.5,
    icon: '🔵'
  },
  cannon: {
    name: 'Cannon Tower',
    cost: 200,
    description: 'High damage, slow attack. Best on lakes',
    damage: 25,
    range: 2.5,
    speed: 0.4,
    icon: '🟡'
  },
  aoe: {
    name: 'AoE Tower',
    cost: 250,
    description: 'Attacks multiple enemies in area',
    damage: 6,
    range: 2.5,
    speed: 0.8,
    icon: '🟣'
  }
}

function TowerMenu({ selectedTower, onTowerSelect, playerMoney }) {
  return (
    <div className="tower-menu">
      <h3>🏰 Build Tower</h3>
      <div className="tower-grid">
        {Object.entries(TOWER_INFO).map(([type, info]) => {
          const canAfford = playerMoney >= info.cost
          const isSelected = selectedTower === type

          return (
            <div
              key={type}
              className={`tower-card ${isSelected ? 'selected' : ''} ${!canAfford ? 'disabled' : ''}`}
              onClick={() => canAfford && onTowerSelect(type)}
            >
              <div className="tower-icon">{info.icon}</div>
              <div className="tower-name">{info.name}</div>
              <div className="tower-cost">💰 {info.cost}</div>
              <div className="tower-stats">
                <div>⚔️ {info.damage}</div>
                <div>📍 {info.range}</div>
                <div>⚡ {info.speed}</div>
              </div>
              <div className="tower-description">{info.description}</div>
            </div>
          )
        })}
      </div>
      <div className="tower-legend">
        <h4>Terrain Bonuses:</h4>
        <p>🏔️ Mountains: +50% range, -30% damage</p>
        <p>💧 Lakes: +50% damage, -40% speed</p>
      </div>
    </div>
  )
}

TowerMenu.propTypes = {
  selectedTower: PropTypes.string.isRequired,
  onTowerSelect: PropTypes.func.isRequired,
  playerMoney: PropTypes.number.isRequired
}

export default TowerMenu

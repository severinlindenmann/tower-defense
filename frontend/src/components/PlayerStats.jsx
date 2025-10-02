import PropTypes from 'prop-types'
import './PlayerStats.css'

function PlayerStats({ player }) {
  if (!player) {
    return (
      <div className="player-stats">
        <h3>Player Stats</h3>
        <p>Loading...</p>
      </div>
    )
  }

  return (
    <div className="player-stats">
      <h3>📊 Player Stats</h3>
      <div className="stats-grid">
        <div className="stat-item">
          <div className="stat-icon">💰</div>
          <div className="stat-info">
            <div className="stat-label">Money</div>
            <div className="stat-value">{player.money}</div>
          </div>
        </div>
        <div className="stat-item">
          <div className="stat-icon">❤️</div>
          <div className="stat-info">
            <div className="stat-label">Lives</div>
            <div className="stat-value">{player.lives}</div>
          </div>
        </div>
        <div className="stat-item">
          <div className="stat-icon">⭐</div>
          <div className="stat-info">
            <div className="stat-label">Points</div>
            <div className="stat-value">{player.points}</div>
          </div>
        </div>
        <div className="stat-item">
          <div className="stat-icon">🏰</div>
          <div className="stat-info">
            <div className="stat-label">Towers</div>
            <div className="stat-value">{player.towers_built}</div>
          </div>
        </div>
        <div className="stat-item">
          <div className="stat-icon">💀</div>
          <div className="stat-info">
            <div className="stat-label">Kills</div>
            <div className="stat-value">{player.enemies_defeated}</div>
          </div>
        </div>
      </div>
    </div>
  )
}

PlayerStats.propTypes = {
  player: PropTypes.shape({
    money: PropTypes.number,
    lives: PropTypes.number,
    points: PropTypes.number,
    towers_built: PropTypes.number,
    enemies_defeated: PropTypes.number
  })
}

export default PlayerStats

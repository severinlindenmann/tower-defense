import PropTypes from 'prop-types'
import './GameControls.css'

function GameControls({ gameStarted, gameOver, onStartGame }) {
  if (gameOver) {
    return (
      <div className="game-controls">
        <div className="game-over">
          <h2>💀 Game Over</h2>
          <p>Thanks for playing!</p>
          <button onClick={() => window.location.reload()}>
            Play Again
          </button>
        </div>
      </div>
    )
  }

  if (!gameStarted) {
    return (
      <div className="game-controls">
        <button className="start-button" onClick={onStartGame}>
          🎮 Start Game
        </button>
      </div>
    )
  }

  return null
}

GameControls.propTypes = {
  gameStarted: PropTypes.bool.isRequired,
  gameOver: PropTypes.bool.isRequired,
  onStartGame: PropTypes.func.isRequired
}

export default GameControls

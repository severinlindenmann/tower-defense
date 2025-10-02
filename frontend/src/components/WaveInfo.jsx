import PropTypes from 'prop-types'
import './WaveInfo.css'

function WaveInfo({ currentWave, waveInProgress, timeToNextWave, enemiesCount }) {
  return (
    <div className="wave-info">
      <h3>🌊 Wave Information</h3>
      <div className="wave-content">
        <div className="wave-number">
          <div className="wave-label">Current Wave</div>
          <div className="wave-value">{currentWave}</div>
        </div>
        
        <div className="wave-status">
          {waveInProgress ? (
            <>
              <div className="status-indicator active"></div>
              <div className="status-text">Wave in Progress</div>
              <div className="enemies-count">👾 {enemiesCount} enemies</div>
            </>
          ) : (
            <>
              <div className="status-indicator waiting"></div>
              <div className="status-text">Preparing...</div>
              <div className="next-wave-timer">
                Next wave in: {Math.ceil(timeToNextWave)}s
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

WaveInfo.propTypes = {
  currentWave: PropTypes.number.isRequired,
  waveInProgress: PropTypes.bool.isRequired,
  timeToNextWave: PropTypes.number.isRequired,
  enemiesCount: PropTypes.number.isRequired
}

export default WaveInfo

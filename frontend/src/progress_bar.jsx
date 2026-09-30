import "./progress_bar.css"

function ProgressBar({ totalCount, currentCount }) {

    if (!totalCount) {
        return null
    }

    const percentage = Math.min(
        100,
        Math.round((currentCount / totalCount) * 100)
    )

    return (
        <div className="progress-container">

            <div className="progress-header">

                <div>
                    <h3>Analyzing Comments</h3>

                    <p>
                        {totalCount == currentCount? "Processing Completed" : "Processing comments..."}
                    </p>
                </div>

                <span className="progress-percentage">
                    {percentage}%
                </span>

            </div>


            <div className="progress-track">

                <div
                    className="progress-fill"
                    style={{
                        width: `${percentage}%`
                    }}
                />

            </div>


            <div className="progress-footer">

                <span>
                    {currentCount} / {totalCount} comments
                </span>

                {currentCount < totalCount && (
                    <span className="processing-indicator">
                        <span className="pulse-dot"></span>
                        Processing
                    </span>
                )}

                {currentCount >= totalCount && (
                    <span className="completed-text">
                        Complete
                    </span>
                )}

            </div>

        </div>
    )
}

export default ProgressBar
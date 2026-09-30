import "./distribution_chart.css"

function DistributionChart({ title, distribution }) {

    if (!distribution) {
        return null
    }

    const entries = Object.entries(distribution)
        .sort((a, b) => b[1] - a[1])

    return (
        <div className="distribution-chart">

            <h3 className="distribution-title">
                {title}
            </h3>

            <div className="distribution-list">

                {entries.map(([label, percentage]) => (

                    <div
                        className="distribution-row"
                        key={label}
                    >

                        <div className="distribution-label">
                            {label}
                        </div>

                        <div className="distribution-bar-container">

                            <div
                                className="distribution-bar"
                                style={{
                                    width: `${percentage}%`
                                }}
                            />

                        </div>

                        <div className="distribution-value">
                            {percentage.toFixed(1)}%
                        </div>

                    </div>

                ))}

            </div>

        </div>
    )
}

export default DistributionChart
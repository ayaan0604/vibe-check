import DistributionChart from "./distribution_chart"
import "./result_section.css"

function ResultSection({ result }) {

    if (!result) {
        return null
    }

    return (
        <section className="result-section">

            {/* Header */}

            <div className="result-header">
                <div>
                    <h2>Analysis Report</h2>
                    <p>Here's what the comments have to say.</p>
                </div>
            </div>


            {/* Main Metrics */}

            <div className="metrics-grid">

                <div className="metric-card">
                    <span className="metric-label">
                        Comments Analyzed
                    </span>

                    <span className="metric-value">
                        {result.total_comments}
                    </span>
                </div>


                <div className="metric-card">
                    <span className="metric-label">
                        Sarcasm Rate
                    </span>

                    <span className="metric-value">
                        {Math.round(result.sarcasm_rate * 100) / 100}%
                    </span>
                </div>


                <div className="metric-card">
                    <span className="metric-label">
                        Vibe
                    </span>

                    <span className="metric-value metric-vibe">
                        {result.vibe}
                    </span>
                </div>


                <div className="metric-card">
                    <span className="metric-label">
                        Chaos Index
                    </span>

                    <span className="metric-value">
                        {result.chaos_index}
                    </span>
                </div>


                <div className="metric-card">
                    <span className="metric-label">
                        Roast / Hype
                    </span>

                    <span className="metric-value">
                        {result.roast_to_hype_ratio}
                    </span>
                </div>

            </div>


            {/* Distributions */}

            <div className="distribution-section">

                <div className="section-heading">
                    <h3>Comment Breakdown</h3>
                    <p>How the comments were classified.</p>
                </div>

                <div className="charts-grid">

                    <div className="chart-card">
                        <DistributionChart
                            title="Intent Distribution"
                            distribution={result.intent_distribution}
                        />
                    </div>

                    <div className="chart-card">
                        <DistributionChart
                            title="Reaction Distribution"
                            distribution={result.reaction_distribution}
                        />
                    </div>

                </div>

            </div>

        </section>
    )
}

export default ResultSection
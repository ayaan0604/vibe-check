import "./about.css"

function AboutSection() {

    return (
        <section className="about-section" id="about">

            <div className="about-content">

                <div className="about-heading">
                    <span className="about-label">
                        ABOUT VIBE CHECK
                    </span>

                    <h2>
                        Understand the vibe behind the comments.
                    </h2>

                    <p>
                        Vibe Check turns an Instagram comment section into
                        structured, readable insights.
                    </p>
                </div>


                <div className="about-grid">

                    <div className="about-card">

                        <span className="about-number">
                            01
                        </span>

                        <h3>
                            Enter an Instagram URL
                        </h3>

                        <p>
                            Give Vibe Check an Instagram post URL and it
                            fetches the most popular comments from the post
                            for analysis.
                        </p>

                    </div>


                    <div className="about-card">

                        <span className="about-number">
                            02
                        </span>

                        <h3>
                            Choose a model
                        </h3>

                        <p>
                            Select the analysis model you want to use.
                            Currently, Vibe Check supports Jev and Laya,
                            each processing the comments and judging them
                            across several characteristics.
                        </p>

                    </div>


                    <div className="about-card">

                        <span className="about-number">
                            03
                        </span>

                        <h3>
                            Get the bigger picture
                        </h3>

                        <p>
                            Each comment is classified by intent, reaction,
                            and sarcasm. The results are then combined into
                            an overall report showing the vibe, chaos index,
                            roast-to-hype ratio, and more.
                        </p>

                    </div>


                    <div className="about-card">

                        <span className="about-number">
                            04
                        </span>

                        <h3>
                            Cached for 24 hours
                        </h3>

                        <p>
                            If the same Instagram URL is analyzed again with
                            the same model within 24 hours, Vibe Check uses
                            its cached analysis instead of fetching and
                            processing everything again.
                        </p>

                    </div>

                </div>


                <div className="about-footer">

                    <div className="about-footer-line"></div>

                    <p>
                        Analyze once. Come back later. The vibe is still there.
                    </p>

                </div>

            </div>

        </section>
    )
}

export default AboutSection
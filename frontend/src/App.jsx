import { useState, useRef, useEffect } from "react"

import Header from "./header"
import URLInput from "./input"
import ProgressBar from "./progress_bar"
import CommentCard from "./comment_card"
import ResultSection from "./result_section"
import AboutSection from "./about"

import "./App.css"


const api_url = "https://vibe-check-o27o.onrender.com/analyze/stream"


function App() {

    const [error, setError] = useState(null)

    const [comments, setComments] = useState([])
    const [report, setReport] = useState(null)

    const [totalComments, setTotalComments] = useState(0)
    const [loading, setLoading] = useState(false)

    const analysisRef = useRef(null)

    async function analyze(url, model) {

        
        setLoading(true)
        setError(null)

        setComments([])
        setReport(null)
        setTotalComments(0)


        


        try {

            if(!url){
                throw new Error("You must provide a url")
            }


            const response = await fetch(
                api_url,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        url: {
                            url: url
                        },
                        model: model
                    })
                }
            )


            if (!response.ok) {
                const errorData = await response.json()

                throw new Error(
                    errorData.detail?.[0]?.msg ||
                    errorData.detail?.error ||
                    "Invalid request"
                )
            }


            if (!response.body) {
                throw new Error(
                    "Response has no body"
                )
            }


            const reader = response.body.getReader()
            const decoder = new TextDecoder()

            let buffer = ""


            while (true) {

                const { value, done } = await reader.read()


                if (done) {
                    break
                }


                buffer += decoder.decode(
                    value,
                    { stream: true }
                )


                while (buffer.includes("\n\n")) {

                    const boundary = buffer.indexOf("\n\n")

                    const event = buffer.slice(
                        0,
                        boundary
                    )

                    buffer = buffer.slice(
                        boundary + 2
                    )


                    const jsonString = event
                        .slice(5)
                        .trim()


                    const data = JSON.parse(jsonString)


                    if (data.type === "cached") {

                        setTotalComments(
                            data.data.total_comments
                        )

                        setComments(
                            data.data.comments
                        )

                        setReport(
                            data.data
                        )
                    }


                    else if (data.type === "starting") {

                        setTotalComments(
                            data.data.comments_fetched
                        )
                    }


                    else if (data.type === "comment") {
                        
                        setComments((prev) => [
                            ...prev,
                            data.data.data
                        ])
                    }

                    else if (data.type === "final_report") {

                        setReport(
                            data.data
                        )
                    }

                    else if (data.type === "error") {

                        setError(
                            data.data.error
                        )
                    }
                }
            }

        } catch (error) {

            setError(error.message)

        } finally {

            setLoading(false)
        }
    }


    /*
     * The analysis workspace should exist as soon
     * as the user starts an analysis.
     *
     * This also works for cached results because
     * report/comments will immediately become available.
     */

    const showAnalysis =
        loading ||
        comments.length > 0 ||
        report !== null


    return (

        <div className="app">

            <Header />


            <main className="main-content">


                <URLInput
                    onAnalyze={analyze}
                />


                {showAnalysis && (

                    <>

                        <ProgressBar
                            totalCount={totalComments}
                            currentCount={comments.length}
                        />


                        <div className="analysis-workspace">


                            <section className="comments-pane">

                                <div className="pane-header">

                                    <div>
                                        <h2>Comments</h2>

                                        <p>
                                            Live analysis
                                        </p>
                                    </div>

                                    <span className="comment-count">
                                        {comments.length}
                                    </span>

                                </div>


                                <div className="comments-scroll">

                                    {comments.length === 0 && loading && (

                                        <div className="comments-empty">

                                            <div className="loading-dot"></div>

                                            <p>
                                                Waiting for comments...
                                            </p>

                                        </div>

                                    )}


                                    {comments.map((comment) => (

                                        <CommentCard
                                            key={comment.comment_id}
                                            comment={comment}
                                        />

                                    ))}

                                </div>

                            </section>


                            <section className="result-pane">

                                {!report && (

                                    <div className="awaiting-result">

                                        <div className="awaiting-icon">
                                            ...
                                        </div>

                                        <h2>
                                            Awaiting Result
                                        </h2>

                                        <p>
                                            The report will appear here
                                            once all comments have been
                                            analyzed.
                                        </p>

                                    </div>

                                )}


                                {report && (

                                    <ResultSection
                                        result={report}
                                    />

                                )}

                            </section>

                        </div>

                    </>

                )}



                {error && (

                    <div className="error-message">

                        <strong>
                            Something went wrong
                        </strong>

                        <span>
                            {error}
                           
                        </span>

                    </div>

                )}

            </main>


            {/* =========================
                ABOUT
               ========================= */}

            <AboutSection />

        </div>
    )
}


export default App
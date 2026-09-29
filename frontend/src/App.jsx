import { useState } from "react";
import URLInput from './input'
import ResultSection from "./result_section";

function App(){
    const[result, setResult] = useState(null)
    const[loading, setLoading] = useState(false)
    const[error, setError] = useState(null)

    async function analyze(url, model){
        setLoading(true)
        setError(null)

        try{
            const response = await fetch(
                "http://127.0.0.1:8000/analyze", {
                    method: "POST",
                    headers: {
                        "Content-Type" : 'application/json'
                    },
                    body : JSON.stringify({
                        url : {
                            url : url
                        },
                        model : model
                    })
                }

            )

            if(!response.ok){
                throw new Error("Api request Failed")
            }

            const data = await response.json()

            setResult(data)

        } catch(error){
            setError(error.message)
        }finally{
            setLoading(false)
        }

    }

    return <div>
        <h1>Comments Analyzer</h1>

        <URLInput onAnalyze={analyze}/>
        {loading && <p>Analyzing...</p>}
        {error && <p>Error: {error}</p>}
        <ResultSection result={result}/>
    </div>

}

export default App
import { useState } from 'react'
import './input.css'

function URLInput({ onAnalyze }) {

    const [selected_model, updateModel] = useState("laya")
    const [entered_url, updateUrl] = useState("")

    return (
        <div className="input-container">

            <div className="input-heading">
                <h2>Vibe Check</h2>
                <p>Enter a URL and choose an analysis model</p>
            </div>

            <div className="form-group">
                <label htmlFor="url">URL</label>

                <input
                    type="text"
                    name="url"
                    id="url"
                    placeholder="https://instagram.com/..."
                    value={entered_url}
                    onChange={(e) => {
                        updateUrl(e.target.value)
                    }}
                />
            </div>

            <div className="form-group">
                <label htmlFor="model">Model</label>

                <select
                    id="model"
                    value={selected_model}
                    onChange={(event) => {
                        updateModel(event.target.value)
                    }}
                >
                    <option value="laya">Laya (slow)</option>
                    <option value="jev">Jev</option>
                </select>
            </div>

            <button
                className="analyze-button"
                onClick={() => {
                    onAnalyze(entered_url, selected_model)
                }}
            >
                Analyze
            </button>

        </div>
    )
}

export default URLInput
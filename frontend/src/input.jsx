import  {useState} from 'react'

function URLInput({ onAnalyze }){

    const [selected_model, updateModel] = useState("laya")
    const [entered_url, updateUrl] = useState("")

    return <div>
        <label htmlFor = "url">Enter the URL</label>
        <input type="text" name="url" id="url" value={entered_url} onChange={
            (e)=>{
                updateUrl(e.target.value)
            }
        } />
        <label htmlFor = 'model'>Select your Model</label>
        <select id = 'model' value={selected_model} onChange={(event)=>{
            updateModel(event.target.value)
        }}>
        <option value= 'laya'>Laya(slow)</option>
        <option value='jev'>Jev</option>


        </select>

        <button onClick={
            ()=>{
                onAnalyze(entered_url, selected_model)
        }}>Analyze</button>
        
    </div>


}

export default URLInput
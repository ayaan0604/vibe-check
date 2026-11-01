const backend_url = 'https://vibe-check-o27o.onrender.com'

let wake_promise = null

export function wakeUpBackend(){

    console.log("waking up backend...")

    if(wake_promise){
        return wake_promise
    }

    wake_promise = fetch(`${backend_url}/health`, {
        method : "GET",
        cache: "no-store"
    })
    .then(
        (response)=>{
            if(!response.ok){
                throw new Error("Backend returned: ", response.status)
            }

            console.log("Backend is awake: ")
            return response
        }
    )
    .catch((error)=>{
        console.warn(error)
    })
    .finally(()=>{
        wake_promise = null
    })

    
}
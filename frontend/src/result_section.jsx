
import CommentCard from "./comment_card"
import DistributionChart from "./distribution_chart"

function ResultSection({result}){

    if(!result){
        return <p>no result yet</p>
    }

    return <div>
        <h2>Analysis Report</h2>

        <p>Total Comments Analyzed: {result.total_comments}</p>
        <p>Sarcasm Rate: {Math.round(result.sarcasm_rate*100)/100}</p>
        <p>Vibe : {result.vibe}</p>
        <p>Chaos Index: {result.chaos_index}</p>
        <p>Roast/Hype : {result.roast_to_hype_ratio}</p>

        <DistributionChart title={"Intent Distribution"} distribution={result.intent_distribution}/>
        <DistributionChart title={"Reaction Distribution"} distribution={result.reaction_distribution}/>

        <h2>Comments</h2>

        <ul>
            {
                result.comments.map((comment)=>{
                    return <li key={comment.id}>
                        <CommentCard comment={comment} />
                    </li>
                })
            }
        </ul>

    </div>

}

export default ResultSection
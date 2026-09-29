function DistributionChart({title, distribution}){


    return <div>
            <h3>{title}</h3>

            {Object.entries(distribution)
            .sort((a,b)=>{return b[1] - a[1] })
            .map(([label, percentage])=>{
                return <div key={label}
                        style = {{
                            display: 'flex',
                            alignItems: 'centre',
                            gap : '10px'
                        }}>

                    <span style = {{width: "100px"}}>
                        {label}
                    </span>

                    
                    <div
                        style = {{
                            width: `${percentage}%`,
                            height : '10px',
                            backgroundColor : 'black'
                        }}
                    />
                    <span> {percentage.toFixed(1)}%</span>
                
                    
                </div>
                
            })}
    </div>

}

export default DistributionChart
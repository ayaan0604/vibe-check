import './comment_card.css'

function CommentCard({ comment }) {

    return (
        <div className="comment-card">

            <p className="comment-text">
                {comment.text}
            </p>

            <div className="comment-badges">

                <span className={`badge intent-${comment.intent}`}>
                    {comment.intent}
                </span>

                <span className={`badge reaction-${comment.reaction}`}>
                    {comment.reaction}
                </span>

                {Boolean(comment.sarcastic) && (
                    <span className="badge sarcastic-badge">
                        Sarcastic
                    </span>
                )}

            </div>

        </div>
    )
}

export default CommentCard
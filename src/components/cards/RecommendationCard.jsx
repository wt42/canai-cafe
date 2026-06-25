export default function RecommendationCard({ recommendation }) {
  return (
    <article className="recommendation-card">
      <div className="recommendation-head">
        <h3>{recommendation.title}</h3>
        <span className={`confidence ${recommendation.confidence?.toLowerCase()}`}>{recommendation.confidence}</span>
      </div>
      <dl>
        <dt>Evidence</dt>
        <dd>{recommendation.evidence}</dd>
        <dt>Action</dt>
        <dd>{recommendation.action}</dd>
        <dt>Expected impact</dt>
        <dd>{recommendation.expectedImpact}</dd>
        <dt>Limitation</dt>
        <dd>{recommendation.limitation}</dd>
      </dl>
    </article>
  );
}

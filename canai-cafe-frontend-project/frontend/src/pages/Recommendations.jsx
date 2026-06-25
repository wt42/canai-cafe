import { useEffect, useState } from 'react';
import PageHeader from '../components/common/PageHeader.jsx';
import LoadingState from '../components/common/LoadingState.jsx';
import ErrorState from '../components/common/ErrorState.jsx';
import RecommendationCard from '../components/cards/RecommendationCard.jsx';
import { getJson } from '../services/dataService.js';

export default function Recommendations() {
  const [recommendations, setRecommendations] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getJson('recommendations.json').then(setRecommendations).catch(setError);
  }, []);

  if (error) return <ErrorState error={error} />;
  if (!recommendations) return <LoadingState />;

  return (
    <>
      <PageHeader
        eyebrow="Recommendation Board"
        title="Business actions from the analysis"
        description="Every recommendation includes evidence, action, expected impact, confidence, and limitation."
      />

      <section className="recommendation-grid">
        {recommendations.map((recommendation) => (
          <RecommendationCard key={recommendation.title} recommendation={recommendation} />
        ))}
      </section>
    </>
  );
}

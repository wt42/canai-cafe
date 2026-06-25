import { useEffect, useState } from 'react';
import PageHeader from '../components/common/PageHeader.jsx';
import LoadingState from '../components/common/LoadingState.jsx';
import ErrorState from '../components/common/ErrorState.jsx';
import MethodologyCard from '../components/cards/MethodologyCard.jsx';
import { getJson } from '../services/dataService.js';

export default function Methodology() {
  const [methodology, setMethodology] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getJson('methodology.json').then(setMethodology).catch(setError);
  }, []);

  if (error) return <ErrorState error={error} />;
  if (!methodology) return <LoadingState />;

  return (
    <>
      <PageHeader
        eyebrow="Methodology"
        title="How the solution works"
        description="A clear explanation of cleaning, analysis, forecasting, and frontend design choices."
      />

      <section className="method-grid">
        {methodology.sections.map((section) => (
          <MethodologyCard key={section.title} section={section} />
        ))}
      </section>
    </>
  );
}

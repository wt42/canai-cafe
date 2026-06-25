import { useEffect, useState } from 'react';
import PageHeader from '../components/common/PageHeader.jsx';
import LoadingState from '../components/common/LoadingState.jsx';
import ErrorState from '../components/common/ErrorState.jsx';
import InsightCard from '../components/cards/InsightCard.jsx';
import { getJson } from '../services/dataService.js';

export default function PowerBIReport() {
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);
  const reportUrl = import.meta.env.VITE_POWERBI_REPORT_URL;

  useEffect(() => {
    getJson('powerbi_report.json').then(setReport).catch(setError);
  }, []);

  if (error) return <ErrorState error={error} />;
  if (!report) return <LoadingState />;

  const finalUrl = reportUrl || report.reportUrl;

  return (
    <>
      <PageHeader
        eyebrow="Power BI Integration"
        title="Dashboard connection point"
        description="Use this page to connect the React portal with your Power BI report or to keep dashboard screenshots as a demo backup."
      />

      <div className="grid two-columns">
        <InsightCard title="Recommended approach" variant="highlight">
          Keep the React portal as the executive story and Power BI as the detailed dashboard. Add a link here when the Power BI report is ready.
        </InsightCard>
        <InsightCard title="Demo safety note">
          Do not depend only on live embedding. Keep screenshots ready in case sharing permissions or internet access fail during judging.
        </InsightCard>
      </div>

      {finalUrl ? (
        <section className="powerbi-box">
          <a className="primary-button" href={finalUrl} target="_blank" rel="noreferrer">Open Power BI Report</a>
          <iframe title="Power BI Report" src={finalUrl} />
        </section>
      ) : (
        <section className="placeholder-panel">
          <h3>No Power BI URL configured yet</h3>
          <p>Add VITE_POWERBI_REPORT_URL in a .env file or update public/data/powerbi_report.json.</p>
          <code>VITE_POWERBI_REPORT_URL=https://your-powerbi-report-link</code>
        </section>
      )}
    </>
  );
}

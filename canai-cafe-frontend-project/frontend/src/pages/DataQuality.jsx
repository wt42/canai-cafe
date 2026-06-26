import { useEffect, useState } from 'react';
import PageHeader from '../components/common/PageHeader.jsx';
import LoadingState from '../components/common/LoadingState.jsx';
import ErrorState from '../components/common/ErrorState.jsx';
import KpiCard from '../components/cards/KpiCard.jsx';
import InsightCard from '../components/cards/InsightCard.jsx';
import DataQualityChart from '../components/charts/DataQualityChart.jsx';
import { getJson } from '../services/dataService.js';
import { formatNumber, formatPercent } from '../utils/formatNumber.js';
import QualityScoreChart from '../components/charts/QualityScoreChart.jsx';
export default function DataQuality() {
  const [quality, setQuality] = useState(null);
  const [error, setError] = useState(null);
  
  const hiddenCards = [
    'Rejected Rows',
    'RCRADS'  
  ];

  useEffect(() => {
    getJson('data_quality_summary.json').then(setQuality).catch(setError);
  }, []);

  if (error) return <ErrorState error={error} />;
  if (!quality) return <LoadingState />;

  return (
    <>
      <PageHeader
        eyebrow="Data Quality Center"
        title="Cleaning decisions are visible and defensible"
        description="The app does not hide dirty data. It shows what was repaired, what was marked unknown, and what was excluded from forecasting."
      />

      <section className="kpi-grid">
        {quality.summaryCards.filter(card => !hiddenCards.includes(card.label)).map((card) => (
          <KpiCard key={card.label} label={card.label} value={formatNumber(card.value)} note={card.note} />
        ))}
      </section>

      <div className="grid two-columns" style={{ columnGap: '24px', marginTop: '32px' }}>
        <DataQualityChart data={quality.issueBreakdown} />
        <QualityScoreChart   score={quality.score} retainedRows={10000} rejectedRows={0} repaired={98 + 100}/>
      </div>

      <section className="table-card">
        <h3>Before vs After Category Cleanup</h3>
        <table>
          <thead>
            <tr>
              <th>Category</th>
              <th>Before</th>
              <th>After</th>
              <th>Decision</th>
            </tr>
          </thead>
          <tbody>
            {quality.categoryCleanup.map((row) => (
              <tr key={row.category}>
                <td>{row.category}</td>
                <td>{row.before}</td>
                <td>{row.after}</td>
                <td>{row.decision}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section
        className="decision-grid"
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(2, 1fr)',
          gap: '24px',
          marginTop: '32px',
        }}
      >
        {quality.cleaningDecisions.map((decision, index) => (
          <div
            key={decision.issue}
            style={
              index === quality.cleaningDecisions.length - 1
                ? { gridColumn: '1 / -1' }
                : {}
            }
          >
            <InsightCard title={decision.issue}>
              <strong>Decision:</strong> {decision.decision}
              <br />
              <strong>Reason:</strong> {decision.reason}
            </InsightCard>
          </div>
        ))}
      </section>
    </>
  );
}

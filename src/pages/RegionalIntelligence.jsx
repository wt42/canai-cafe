import { useEffect, useState } from 'react';
import PageHeader from '../components/common/PageHeader.jsx';
import LoadingState from '../components/common/LoadingState.jsx';
import ErrorState from '../components/common/ErrorState.jsx';
import InsightCard from '../components/cards/InsightCard.jsx';
import BarChartPanel from '../components/charts/BarChartPanel.jsx';
import { getJson } from '../services/dataService.js';
import { formatCurrency } from '../utils/formatCurrency.js';
import { formatNumber, formatPercent } from '../utils/formatNumber.js';

export default function RegionalIntelligence() {
  const [provinces, setProvinces] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getJson('province_performance.json').then(setProvinces).catch(setError);
  }, []);

  if (error) return <ErrorState error={error} />;
  if (!provinces) return <LoadingState />;

  const topProvince = provinces[0];
  const unknown = provinces.find((item) => item.name === 'Unknown Province');

  return (
    <>
      <PageHeader
        eyebrow="Regional Intelligence"
        title="Province-level performance"
        description="Regional analysis uses cleaned province names while keeping Unknown Province visible for transparency."
      />

      <div className="grid three-columns">
        <InsightCard title="Top region" variant="highlight">
          {topProvince.name} generated {formatCurrency(topProvince.revenue)} and leads the regional ranking.
        </InsightCard>
        <InsightCard title="Unknown impact">
          {unknown ? `${formatCurrency(unknown.revenue)} is assigned to Unknown Province and should stay visible.` : 'No unknown province impact found.'}
        </InsightCard>
        <InsightCard title="Honest interpretation">
          Ontario has very low volume, so it should be shown but not over-interpreted as a major market signal.
        </InsightCard>
      </div>

      <BarChartPanel title="Revenue by Province" subtitle="Cleaned regional performance" data={provinces} />

      <section className="table-card">
        <h3>Province Ranking</h3>
        <table>
          <thead>
            <tr>
              <th>Province</th>
              <th>Revenue</th>
              <th>Transactions</th>
              <th>Units</th>
              <th>Revenue Share</th>
            </tr>
          </thead>
          <tbody>
            {provinces.map((province) => (
              <tr key={province.name}>
                <td>{province.name}</td>
                <td>{formatCurrency(province.revenue)}</td>
                <td>{formatNumber(province.transactions)}</td>
                <td>{formatNumber(province.units)}</td>
                <td>{formatPercent(province.revenueShare)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </>
  );
}

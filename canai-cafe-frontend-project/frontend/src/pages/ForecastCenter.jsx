import { useEffect, useState } from 'react';
import PageHeader from '../components/common/PageHeader.jsx';
import LoadingState from '../components/common/LoadingState.jsx';
import ErrorState from '../components/common/ErrorState.jsx';
import KpiCard from '../components/cards/KpiCard.jsx';
import InsightCard from '../components/cards/InsightCard.jsx';
import ForecastChart from '../components/charts/ForecastChart.jsx';
import { getJson } from '../services/dataService.js';
import { formatCurrency } from '../utils/formatCurrency.js';

export default function ForecastCenter() {
  const [forecast, setForecast] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getJson('forecast_6_months.json').then(setForecast).catch(setError);
  }, []);

  if (error) return <ErrorState error={error} />;
  if (!forecast) return <LoadingState />;

  return (
    <>
      <PageHeader
        eyebrow="Forecast Center"
        title="Six-month sales forecast"
        description="A baseline planning forecast for January to June 2024 using cleaned 2023 transaction data."
      />

      <section className="kpi-grid small-grid">
        <KpiCard label="Model" value={forecast.modelName} note="Explainable and hackathon-safe" />
        <KpiCard label="Forecast Period" value={forecast.forecastPeriod} note="Next six months" />
        <KpiCard label="Total Forecast" value={formatCurrency(forecast.totalForecastRevenue)} note="Baseline planning view" />
        <KpiCard label="Daily MAE" value={forecast.validation.mae} note="Validation metric" />
        <KpiCard label="Daily RMSE" value={forecast.validation.rmse} note="Validation metric" />
      </section>

      <ForecastChart data={forecast.monthlyForecast} />

      <section className="table-card">
        <h3>Forecast Table</h3>
        <table>
          <thead>
            <tr>
              <th>Month</th>
              <th>Forecast Revenue</th>
              <th>Lower Estimate</th>
              <th>Upper Estimate</th>
              <th>Planning Note</th>
            </tr>
          </thead>
          <tbody>
            {forecast.monthlyForecast.map((row) => (
              <tr key={row.month}>
                <td>{row.month}</td>
                <td>{formatCurrency(row.forecastRevenue)}</td>
                <td>{formatCurrency(row.lowerEstimate)}</td>
                <td>{formatCurrency(row.upperEstimate)}</td>
                <td>{row.planningNote}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <div className="grid two-columns">
        <InsightCard title="Assumptions" variant="highlight">
          <ul>
            {forecast.assumptions.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </InsightCard>
        <InsightCard title="Limitations">
          <ul>
            {forecast.limitations.map((item) => <li key={item}>{item}</li>)}
          </ul>
        </InsightCard>
      </div>
    </>
  );
}

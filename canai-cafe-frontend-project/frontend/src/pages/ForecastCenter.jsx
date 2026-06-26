import { useEffect, useMemo, useState } from 'react';
import PageHeader from '../components/common/PageHeader.jsx';
import LoadingState from '../components/common/LoadingState.jsx';
import ErrorState from '../components/common/ErrorState.jsx';
import KpiCard from '../components/cards/KpiCard.jsx';
import InsightCard from '../components/cards/InsightCard.jsx';
import ForecastChart from '../components/charts/ForecastChart.jsx';
import BarChartPanel from '../components/charts/BarChartPanel.jsx';
import { getJson } from '../services/dataService.js';
import { formatCurrency } from '../utils/formatCurrency.js';
import { formatNumber, formatPercent } from '../utils/formatNumber.js';
import { chartNumberFormatter } from '../utils/chartHelpers.js';

const VIEW_MODES = {
  daily: {
    label: '30-day daily',
    chartTitle: '30-Day Daily Forecast',
    chartSubtitle: 'Expected daily revenue for the first 30 forecast days',
    defaultBreakdownKey: 'first30',
    summaryKey: 'first30Days',
    comparisonKey: 'recent30Days'
  },
  monthly: {
    label: '6-month monthly',
    chartTitle: '6-Month Monthly Forecast',
    chartSubtitle: 'Expected monthly revenue across the 180-day horizon',
    defaultBreakdownKey: 'full180',
    summaryKey: 'full180Days',
    comparisonKey: 'recent180Days'
  }
};

function selectedPeriodLabel(mode, selectedRow, forecast) {
  if (selectedRow) return selectedRow.label || selectedRow.month || selectedRow.date;
  return mode === 'daily'
    ? `${forecast.horizon.startDate} to ${forecast.dailyForecast[29].date}`
    : forecast.forecastPeriod;
}

function comparisonText(comparison) {
  const basis = comparison.label.replace('Compared with ', '');
  if (comparison.difference === 0) return `Same as ${basis}`;
  const direction = comparison.difference > 0 ? 'higher' : 'lower';
  return `${formatCurrency(Math.abs(comparison.difference))} ${direction} than ${basis}`;
}

function validationMetric(mode, validation) {
  if (mode === 'monthly') {
    return {
      label: 'Typical Monthly Error',
      value: validation.monthlyMae,
      note: 'Average 30-day total error in back-testing'
    };
  }

  return {
    label: 'Typical Daily Error',
    value: validation.mae,
    note: 'Average daily error in back-testing'
  };
}

export default function ForecastCenter() {
  const [forecast, setForecast] = useState(null);
  const [error, setError] = useState(null);
  const [mode, setMode] = useState('daily');
  const [selectedKey, setSelectedKey] = useState(null);

  useEffect(() => {
    getJson('forecast_sales.json').then(setForecast).catch(setError);
  }, []);

  const activeConfig = VIEW_MODES[mode];

  const chartData = useMemo(() => {
    if (!forecast) return [];
    return mode === 'daily'
      ? forecast.dailyForecast.slice(0, 30)
      : forecast.monthlyForecast;
  }, [forecast, mode]);

  const selectedRow = useMemo(() => {
    if (!selectedKey) return null;
    return chartData.find((row) => (mode === 'daily' ? row.date : row.month) === selectedKey) || null;
  }, [chartData, mode, selectedKey]);

  const activeBreakdown = useMemo(() => {
    if (!forecast) return null;
    if (selectedRow && mode === 'daily') return forecast.breakdowns.days[selectedRow.date];
    if (selectedRow && mode === 'monthly') return forecast.breakdowns.months[selectedRow.month];
    return forecast.breakdowns.windows[activeConfig.defaultBreakdownKey];
  }, [activeConfig.defaultBreakdownKey, forecast, mode, selectedRow]);

  if (error) return <ErrorState error={error} />;
  if (!forecast || !activeBreakdown) return <LoadingState />;

  const activeSummary = selectedRow
    ? {
        expectedRevenue: activeBreakdown.totalRevenue,
        averageDailyRevenue: activeBreakdown.averageDailyRevenue,
        days: activeBreakdown.days
      }
    : forecast.summaryMetrics[activeConfig.summaryKey];
  const comparison = forecast.comparisons[activeConfig.comparisonKey];
  const periodLabel = selectedPeriodLabel(mode, selectedRow, forecast);
  const validation = validationMetric(mode, forecast.validation);

  return (
    <>
      <PageHeader
        eyebrow="Forecast Center"
<<<<<<< HEAD
        title="Sales forecast"
        description="A planning forecast generated from cleaned 2023 transactions."
      />

      <section className="forecast-toolbar">
        <div className="segmented-control" aria-label="Forecast view">
          {Object.entries(VIEW_MODES).map(([key, config]) => (
            <button
              key={key}
              type="button"
              className={`segment-button ${mode === key ? 'active' : ''}`}
              onClick={() => {
                setMode(key);
                setSelectedKey(null);
              }}
            >
              {config.label}
            </button>
          ))}
        </div>
        {selectedKey && (
          <button type="button" className="secondary-button" onClick={() => setSelectedKey(null)}>
            Clear selection
          </button>
        )}
      </section>

      <section className="kpi-grid">
        <KpiCard label="Expected Revenue" value={formatCurrency(activeSummary.expectedRevenue)} note={periodLabel} />
        <KpiCard label="Average Daily Revenue" value={formatCurrency(activeSummary.averageDailyRevenue)} note={`${activeSummary.days} forecast days`} />
        <KpiCard label={validation.label} value={formatCurrency(validation.value)} note={validation.note} />
        <KpiCard label="Forecast vs Recent" value={formatPercent(comparison.percentChange)} note={comparisonText(comparison)} />
      </section>

      <ForecastChart
        data={chartData}
        title={activeConfig.chartTitle}
        subtitle={activeConfig.chartSubtitle}
        xKey="label"
        onPointSelect={(row) => setSelectedKey(mode === 'daily' ? row.date : row.month)}
      />

      <div className="grid three-columns forecast-breakdowns">
        <BarChartPanel
          title="Known-Province Revenue"
          subtitle={`${formatCurrency(activeBreakdown.excludedProvince.revenue)} Unknown Province excluded`}
          data={activeBreakdown.provinceRevenue}
        />
        <BarChartPanel
          title="Item Revenue"
          subtitle="Reconciled to selected forecast revenue"
          data={activeBreakdown.itemRevenue}
        />
        <BarChartPanel
          title="Units by Item"
          subtitle="Estimated from forecast revenue and median item price"
          data={activeBreakdown.itemUnits}
          yKey="units"
          valueFormatter={chartNumberFormatter}
        />
      </div>

      <div className="grid">
        <InsightCard title="Model" variant="highlight">
          This forecast looks at 2023 daily sales patterns, especially weekday behavior and recent sales levels, then projects revenue for the next 180 days. It was back-tested on late-2023 holdout periods, where the typical daily miss was {formatCurrency(forecast.validation.mae)}. The model output is generated ahead of time and loaded here as static JSON.
=======
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
>>>>>>> origin/feature/setup-frontend-dashboard
        </InsightCard>
      </div>
    </>
  );
}

import { useEffect, useState } from 'react';
import PageHeader from '../components/common/PageHeader.jsx';
import LoadingState from '../components/common/LoadingState.jsx';
import ErrorState from '../components/common/ErrorState.jsx';
import KpiCard from '../components/cards/KpiCard.jsx';
import InsightCard from '../components/cards/InsightCard.jsx';
import MonthlySalesChart from '../components/charts/MonthlySalesChart.jsx';
import BarChartPanel from '../components/charts/BarChartPanel.jsx';
import ForecastChart from '../components/charts/ForecastChart.jsx';
import { getManyJson } from '../services/dataService.js';
import { formatCurrency } from '../utils/formatCurrency.js';
import { formatNumber, formatPercent } from '../utils/formatNumber.js';
import PieChartPanel from '../components/charts/RevenuePieChart.jsx';

export default function ExecutiveOverview() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getManyJson(['kpi_summary.json', 'monthly_sales.json', 'product_performance.json', 'province_performance.json', 'forecast_sales.json'])
      .then(setData)
      .catch(setError);
  }, []);

  if (error) return <ErrorState error={error} />;
  if (!data) return <LoadingState />;

  const kpi = data['kpi_summary.json'];
  const products = data['product_performance.json'].slice(0, 5);
  const provinces = data['province_performance.json'].slice(0, 5);
  const forecast = data['forecast_sales.json'];

  return (
    <>
      <PageHeader
        eyebrow="Executive Overview"
        title="CanAI Café sales intelligence in one place"
      />

      <section className="kpi-grid">
        <KpiCard label="Total Revenue" value={formatCurrency(kpi.totalRevenue)} note="Cleaned 2023 revenue" />
        <KpiCard label="Transactions" value={formatNumber(kpi.totalTransactions)} note="Rows retained after cleaning" />
        <KpiCard label="Units Sold" value={formatNumber(kpi.totalUnitsSold)} note="Total quantity sold" />
        <KpiCard label="Average Ticket" value={formatCurrency(kpi.averageTransactionValue)} note="Revenue per transaction" />
        <KpiCard label="Top Product" value={kpi.topProduct} note="Highest revenue product" />
        <KpiCard label="Top Province" value={kpi.topProvince} note="Highest revenue province" />
        <KpiCard label="6-Month Forecast" value={formatCurrency(kpi.sixMonthForecast)} note="Jan-Jun 2024 baseline" />
        <KpiCard label="Data Quality Score" value={formatPercent(kpi.dataQualityScore)} note="Rows without quality flags" />
      </section>

      <div className="grid two-columns">
        <MonthlySalesChart data={data['monthly_sales.json']} />
        <PieChartPanel title="Top Product Revenue" subtitle="Revenue leaders after item cleanup" data={products}  xKey = 'name' yKey = 'revenue'/>
      </div>

      <div className="grid two-columns">
        <BarChartPanel title="Top Province Revenue" subtitle="Regional performance after province cleanup" data={provinces} />
        <ForecastChart data={forecast.monthlyForecast} />
      </div>
      <div className="grid three-columns">
        <InsightCard title="Core finding" variant="highlight">
          Coffee drives transaction volume, while Sandwich drives the highest revenue. This creates a strong bundle opportunity.
        </InsightCard>
        <InsightCard title="Forecast position">
          The six-month forecast is stable and should be treated as a planning baseline because only one year of history is available.
        </InsightCard>
        <InsightCard title="Decision focus">
          Management should focus on bundles, weekend demand improvement, high-value product availability, and cleaner data capture.
        </InsightCard>
      </div>
      
    </>
  );
}

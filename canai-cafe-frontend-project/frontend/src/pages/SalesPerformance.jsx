import { useEffect, useState } from 'react';
import PageHeader from '../components/common/PageHeader.jsx';
import LoadingState from '../components/common/LoadingState.jsx';
import ErrorState from '../components/common/ErrorState.jsx';
import InsightCard from '../components/cards/InsightCard.jsx';
import MonthlySalesChart from '../components/charts/MonthlySalesChart.jsx';
import WeekdayWeekendChart from '../components/charts/WeekdayWeekendChart.jsx';
import BarChartPanel from '../components/charts/BarChartPanel.jsx';
import { getManyJson } from '../services/dataService.js';
import { formatCurrency } from '../utils/formatCurrency.js';

export default function SalesPerformance() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getManyJson(['monthly_sales.json', 'weekday_weekend.json', 'weekday_detail.json']).then(setData).catch(setError);
  }, []);

  if (error) return <ErrorState error={error} />;
  if (!data) return <LoadingState />;

  const monthly = data['monthly_sales.json'];
  const bestMonth = [...monthly].sort((a, b) => b.revenue - a.revenue)[0];
  const weakestMonth = [...monthly].sort((a, b) => a.revenue - b.revenue)[0];

  return (
    <>
      <PageHeader
        eyebrow="Sales Performance"
        title="Historical sales performance"      />

      <div className="grid three-columns" >
        <InsightCard title="Highest Revenue Month" variant="highlight">
          {bestMonth.month} generated {formatCurrency(bestMonth.revenue)} in revenue.
        </InsightCard>
        <InsightCard title="Highest Revenue Month">
          {weakestMonth.month} generated {formatCurrency(weakestMonth.revenue)} in revenue.
        </InsightCard>
        <InsightCard title="Analysis Constraints">
          The dataset does not include store hours, promotions, footfall, weather, or inventory. We should not invent causes for monthly movement.
        </InsightCard>
      </div>

      <MonthlySalesChart data={monthly} />

      <div className="grid two-columns" style={{ marginTop: '30px' }}>
        <WeekdayWeekendChart data={data['weekday_weekend.json']} />
        <BarChartPanel title="Average Daily Revenue by Weekday" subtitle="Monday-Friday are much stronger than weekends" data={data['weekday_detail.json']} xKey="name" yKey="avgDailyRevenue" />
      </div>
    </>
  );
}

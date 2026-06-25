import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import ChartFrame from './ChartFrame.jsx';
import { chartCurrencyFormatter } from '../../utils/chartHelpers.js';

export default function WeekdayWeekendChart({ data }) {
  return (
    <ChartFrame title="Weekday vs Weekend" subtitle="Average daily revenue shows a strong weekday/weekend gap">
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 15, right: 20, left: 10, bottom: 10 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis tickFormatter={chartCurrencyFormatter} />
          <Tooltip formatter={(value) => chartCurrencyFormatter(value)} />
          <Bar dataKey="avgDailyRevenue" radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </ChartFrame>
  );
}

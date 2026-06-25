import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import ChartFrame from './ChartFrame.jsx';
import { chartCurrencyFormatter } from '../../utils/chartHelpers.js';

export default function BarChartPanel({ title, subtitle, data, xKey = 'name', yKey = 'revenue' }) {
  return (
    <ChartFrame title={title} subtitle={subtitle}>
      <ResponsiveContainer width="100%" height={320}>
        <BarChart data={data} margin={{ top: 15, right: 20, left: 10, bottom: 70 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={xKey} angle={-35} textAnchor="end" interval={0} />
          <YAxis tickFormatter={chartCurrencyFormatter} />
          <Tooltip formatter={(value) => chartCurrencyFormatter(value)} />
          <Bar dataKey={yKey} radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </ChartFrame>
  );
}

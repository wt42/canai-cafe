import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import ChartFrame from './ChartFrame.jsx';
import { chartCurrencyFormatter } from '../../utils/chartHelpers.js';

export default function MonthlySalesChart({ data }) {
  return (
    <ChartFrame title="Monthly Sales Trend" subtitle="Revenue by month for valid transaction dates">
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data} margin={{ top: 15, right: 20, left: 10, bottom: 10 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis tickFormatter={chartCurrencyFormatter} />
          <Tooltip formatter={(value) => chartCurrencyFormatter(value)} />
          <Line type="monotone" dataKey="revenue" strokeWidth={3} dot={{ r: 4 }} />
        </LineChart>
      </ResponsiveContainer>
    </ChartFrame>
  );
}

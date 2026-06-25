import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import ChartFrame from './ChartFrame.jsx';
import { chartNumberFormatter } from '../../utils/chartHelpers.js';

export default function DataQualityChart({ data }) {
  return (
    <ChartFrame title="Data Quality Issue Breakdown" subtitle="Rows affected by each cleaning decision">
      <ResponsiveContainer width="100%" height={330}>
        <BarChart data={data} margin={{ top: 15, right: 20, left: 10, bottom: 80 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" angle={-35} textAnchor="end" interval={0} />
          <YAxis tickFormatter={chartNumberFormatter} />
          <Tooltip formatter={(value) => chartNumberFormatter(value)} />
          <Bar dataKey="count" radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </ChartFrame>
  );
}

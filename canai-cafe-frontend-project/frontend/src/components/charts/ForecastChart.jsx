import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import ChartFrame from './ChartFrame.jsx';
import { chartCurrencyFormatter } from '../../utils/chartHelpers.js';

export default function ForecastChart({ data }) {
  return (
    <ChartFrame title="Six-Month Forecast" subtitle="Forecast with conservative lower and upper planning range">
      <ResponsiveContainer width="100%" height={320}>
        <LineChart data={data} margin={{ top: 15, right: 20, left: 10, bottom: 10 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="month" />
          <YAxis tickFormatter={chartCurrencyFormatter} />
          <Tooltip formatter={(value) => chartCurrencyFormatter(value)} />
          <Line type="monotone" dataKey="lowerEstimate" strokeWidth={2} strokeDasharray="5 5" name="Lower estimate" />
          <Line type="monotone" dataKey="forecastRevenue" strokeWidth={3} name="Forecast" />
          <Line type="monotone" dataKey="upperEstimate" strokeWidth={2} strokeDasharray="5 5" name="Upper estimate" />
        </LineChart>
      </ResponsiveContainer>
    </ChartFrame>
  );
}

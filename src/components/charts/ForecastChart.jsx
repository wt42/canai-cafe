import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';
import ChartFrame from './ChartFrame.jsx';
import { chartCurrencyFormatter } from '../../utils/chartHelpers.js';

export default function ForecastChart({
  data,
  title = 'Forecast',
  subtitle = 'Expected revenue with conservative lower and upper planning range',
  xKey = 'label',
  onPointSelect
}) {
  return (
    <ChartFrame title={title} subtitle={subtitle}>
      <ResponsiveContainer width="100%" height={320}>
        <LineChart
          data={data}
          margin={{ top: 15, right: 20, left: 10, bottom: 10 }}
          onClick={(state) => {
            const row = state?.activePayload?.[0]?.payload;
            if (row && onPointSelect) onPointSelect(row);
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={xKey} interval="preserveStartEnd" />
          <YAxis tickFormatter={chartCurrencyFormatter} />
          <Tooltip formatter={(value) => chartCurrencyFormatter(value)} />
          <Line type="monotone" dataKey="lowerEstimate" strokeWidth={2} strokeDasharray="5 5" name="Lower estimate" dot={false} />
          <Line type="monotone" dataKey="forecastRevenue" strokeWidth={3} name="Forecast" dot={{ r: 2 }} activeDot={{ r: 6 }} />
          <Line type="monotone" dataKey="upperEstimate" strokeWidth={2} strokeDasharray="5 5" name="Upper estimate" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </ChartFrame>
  );
}

import {  ResponsiveContainer, XAxis, YAxis ,PieChart, Pie, Tooltip, Cell,Legend} from 'recharts';
import ChartFrame from './ChartFrame.jsx';
import { chartCurrencyFormatter } from '../../utils/chartHelpers.js';
import { useState } from 'react';

export default function PieChartPanel({ title, subtitle, data, xKey = 'name', yKey = 'revenue' }) {
  const [activeIndex, setActiveIndex] = useState(-1);
  const onPieEnter = (_, index) => {
        setActiveIndex(index);
    };
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#bb6ba7'];
  const renderLabel = ({ percent }) =>
  `${(percent * 100).toFixed(1)}%`;
  return (
    <ChartFrame title={title} subtitle={subtitle}>
      <ResponsiveContainer width="100%" height={320}>
        
        <PieChart width="100%" height={320}>
            <Pie
                activeIndex={activeIndex}
                data={data}
                dataKey={yKey}
                nameKey={xKey}
                outerRadius={100}
                label={renderLabel}
                labelLine={false}
                fill="green"
                onMouseEnter={onPieEnter}
                style={{ cursor: 'pointer', outline: 'none' }} 
            >
                {data.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
            </Pie>
            <Legend
                verticalAlign="bottom"
                height={36}
            />
            <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </ChartFrame>
  );
}

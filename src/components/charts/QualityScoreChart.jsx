import { PieChart,Pie, Cell, ResponsiveContainer } from 'recharts';
import ChartFrame from './ChartFrame.jsx';
export default function QualityScoreChart({ score ,retainedRows, rejectedRows, repaired}) {
  const data = [
    { name: 'Good', value: score },
    { name: 'Flagged', value: 100 - score }
  ];

  return (
    <ChartFrame
      title="Overall Quality Score"
      subtitle="Percentage of rows without quality flags"
    >
      <div className="chart-card" style={{ position: 'relative', padding: '20px' }}>
        <div style={{ position: 'relative', width: '100%', height: 300 }}>
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={data} dataKey="value" innerRadius={80} outerRadius={100} startAngle={90} endAngle={-270} cornerRadius={10}>
                <Cell fill="#5b341f" />
                <Cell fill="#ffff" />
              </Pie>
            </PieChart>
          </ResponsiveContainer>
            <div style={{ position: 'absolute', top: '50%',  left: '50%',transform: 'translate(-50%, -50%)',textAlign: 'center' }} >
              <h2 style={{ margin: 0 }}>{score.toFixed(2)}%</h2>
              <p style={{ margin: 0, color: '#2c1810', fontWeight: '500' }}>
                  High Quality
              </p>
            </div>
        </div>
        <div style={{ position: 'absolute', bottom: '16px', left: '20px', fontSize: '14px', lineHeight: '1.6' }}>
          <div>✓ Rows retained: <strong>{retainedRows.toLocaleString()}</strong></div>
          <div>✓ Rows rejected: <strong>{rejectedRows}</strong></div>
          <div>✓ Values repaired: <strong>{repaired}</strong></div>
          <div>✓ Quality flags: <strong>{(100 - score).toFixed(2)}%</strong></div>
        </div>
      </div>
    </ChartFrame>
  );
}

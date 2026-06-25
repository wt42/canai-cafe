export default function ChartFrame({ title, subtitle, children }) {
  return (
    <section className="chart-frame">
      <div className="chart-header">
        <h3>{title}</h3>
        {subtitle && <p>{subtitle}</p>}
      </div>
      <div className="chart-body">{children}</div>
    </section>
  );
}

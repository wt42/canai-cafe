export default function KpiCard({ label, value, note }) {
  return (
    <article className="kpi-card">
      <p>{label}</p>
      <h3>{value}</h3>
      {note && <span>{note}</span>}
    </article>
  );
}

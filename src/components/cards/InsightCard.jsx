export default function InsightCard({ title, children, variant = 'default' }) {
  return (
    <article className={`insight-card ${variant}`}>
      <h3>{title}</h3>
      <div>{children}</div>
    </article>
  );
}

export default function MethodologyCard({ section }) {
  return (
    <article className="method-card">
      <h3>{section.title}</h3>
      <ul>
        {section.points.map((point) => (
          <li key={point}>{point}</li>
        ))}
      </ul>
    </article>
  );
}

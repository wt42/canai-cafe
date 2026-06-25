export default function PageHeader({ eyebrow, title, description }) {
  return (
    <section className="page-header">
      {eyebrow && <p className="eyebrow">{eyebrow}</p>}
      <h1>{title}</h1>
      {description && <p>{description}</p>}
    </section>
  );
}

export default function ErrorState({ error }) {
  return (
    <div className="state-card error">
      <strong>Something went wrong</strong>
      <span>{error?.message || 'Unable to load this section.'}</span>
    </div>
  );
}

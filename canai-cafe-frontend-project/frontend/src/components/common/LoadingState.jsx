export default function LoadingState({ message = 'Loading dashboard data...' }) {
  return <div className="state-card loading">{message}</div>;
}

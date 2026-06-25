export function formatNumber(value) {
  return new Intl.NumberFormat('en-CA').format(Number(value || 0));
}

export function formatPercent(value) {
  return `${Number(value || 0).toFixed(2)}%`;
}

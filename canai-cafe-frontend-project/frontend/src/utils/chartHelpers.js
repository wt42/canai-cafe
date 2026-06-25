export const chartCurrencyFormatter = (value) => `$${Number(value || 0).toLocaleString('en-CA')}`;
export const chartNumberFormatter = (value) => Number(value || 0).toLocaleString('en-CA');

import { useEffect, useState } from 'react';
import PageHeader from '../components/common/PageHeader.jsx';
import LoadingState from '../components/common/LoadingState.jsx';
import ErrorState from '../components/common/ErrorState.jsx';
import InsightCard from '../components/cards/InsightCard.jsx';
import BarChartPanel from '../components/charts/BarChartPanel.jsx';
import { getJson } from '../services/dataService.js';
import { formatCurrency } from '../utils/formatCurrency.js';
import { formatNumber, formatPercent } from '../utils/formatNumber.js';

export default function ProductIntelligence() {
  const [products, setProducts] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getJson('product_performance.json').then(setProducts).catch(setError);
  }, []);

  if (error) return <ErrorState error={error} />;
  if (!products) return <LoadingState />;

  const topRevenue = products[0];
  const topVolume = [...products].sort((a, b) => b.transactions - a.transactions)[0];

  return (
    <>
      <PageHeader
        eyebrow="Product Intelligence"
        title="Product mix and revenue opportunity"
        description="This page connects product performance with business actions such as bundles and add-ons."
      />

      <div className="grid three-columns">
        <InsightCard title="Revenue leader" variant="highlight">
          {topRevenue.name} generated {formatCurrency(topRevenue.revenue)} and contributes {formatPercent(topRevenue.revenueShare)} of cleaned revenue.
        </InsightCard>
        <InsightCard title="Volume leader">
          {topVolume.name} has the highest transaction count with {formatNumber(topVolume.transactions)} transactions.
        </InsightCard>
        <InsightCard title="Business move">
          Use Coffee as the traffic product and Sandwich as the basket-value product. This supports a Coffee + Sandwich bundle.
        </InsightCard>
      </div>

      <div className="grid two-columns">
        <BarChartPanel title="Revenue by Product" subtitle="Highest revenue products after item cleanup" data={products} />
        <BarChartPanel title="Transactions by Product" subtitle="Product volume, not just revenue" data={products} yKey="transactions" />
      </div>

      <section className="table-card">
        <h3>Product Ranking</h3>
        <table>
          <thead>
            <tr>
              <th>Product</th>
              <th>Revenue</th>
              <th>Transactions</th>
              <th>Units</th>
              <th>Revenue Share</th>
            </tr>
          </thead>
          <tbody>
            {products.map((product) => (
              <tr key={product.name}>
                <td>{product.name}</td>
                <td>{formatCurrency(product.revenue)}</td>
                <td>{formatNumber(product.transactions)}</td>
                <td>{formatNumber(product.units)}</td>
                <td>{formatPercent(product.revenueShare)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </>
  );
}

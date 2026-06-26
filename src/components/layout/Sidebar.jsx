import { NavLink } from 'react-router-dom';

const links = [
  { to: '/overview', label: 'Executive Overview', icon: '📊' },
  { to: '/sales', label: 'Sales Performance', icon: '📈' },
  { to: '/data-quality', label: 'Data Quality', icon: '🧹' },
  { to: '/products', label: 'Products', icon: '☕' },
  { to: '/regions', label: 'Regions', icon: '🗺️' },
  { to: '/forecast', label: 'Forecast', icon: '🔮' },
  { to: '/recommendations', label: 'Recommendations', icon: '✅' },
  { to: '/methodology', label: 'Methodology', icon: '📝' },
  // { to: '/powerbi', label: 'Power BI', icon: '🖥️' }
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brand-block">
        <div className="brand-icon">C</div>
        <div>
          <h1>CanAI Café</h1>
          <p>Intelligence Portal</p>
        </div>
      </div>

      <nav className="nav-list">
        {links.map((link) => (
          <NavLink key={link.to} to={link.to} className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}>
            <span>{link.icon}</span>
            <span>{link.label}</span>
          </NavLink>
        ))}
      </nav>

      
    </aside>
  );
}

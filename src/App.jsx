import { Navigate, Route, Routes } from 'react-router-dom';
import AppLayout from './components/layout/AppLayout.jsx';
import ChatWidget from './components/chat/ChatWidget.jsx';
import ExecutiveOverview from './pages/ExecutiveOverview.jsx';
import DataQuality from './pages/DataQuality.jsx';
import SalesPerformance from './pages/SalesPerformance.jsx';
import ProductIntelligence from './pages/ProductIntelligence.jsx';
import RegionalIntelligence from './pages/RegionalIntelligence.jsx';
import ForecastCenter from './pages/ForecastCenter.jsx';
import Recommendations from './pages/Recommendations.jsx';
import Methodology from './pages/Methodology.jsx';
import PowerBIReport from './pages/PowerBIReport.jsx';

export default function App() {
  return (
    <AppLayout>
      <Routes>
        <Route path="/" element={<Navigate to="/overview" replace />} />
        <Route path="/overview" element={<ExecutiveOverview />} />
        <Route path="/data-quality" element={<DataQuality />} />
        <Route path="/sales" element={<SalesPerformance />} />
        <Route path="/products" element={<ProductIntelligence />} />
        <Route path="/regions" element={<RegionalIntelligence />} />
        <Route path="/forecast" element={<ForecastCenter />} />
        <Route path="/recommendations" element={<Recommendations />} />
        <Route path="/methodology" element={<Methodology />} />
        <Route path="/powerbi" element={<PowerBIReport />} />
      </Routes>
      <ChatWidget />
    </AppLayout>
  );
}

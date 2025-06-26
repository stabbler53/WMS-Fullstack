import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Inventory from './pages/Inventory';
import Inbound from './pages/Inbound';
import Outbound from './pages/Outbound';
import UploadCSV from './pages/UploadCSV';
import MainLayout from './layouts/MainLayout';

function App() {
  return (
    <Router>
      <Routes>
        {/* Login: no navbar */}
        <Route path="/login" element={<Login />} />

        {/* Protected routes with layout */}
        <Route element={<MainLayout />}>
          <Route path="/inventory" element={<Inventory />} />
          <Route path="/inbound" element={<Inbound />} />
          <Route path="/outbound" element={<Outbound />} />
          <Route path="/upload-csv" element={<UploadCSV />} />
        </Route>

        {/* Default redirect */}
        <Route path="*" element={<Login />} />
      </Routes>
    </Router>
  );
}

export default App;

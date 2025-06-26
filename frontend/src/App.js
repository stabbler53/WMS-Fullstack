import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Login from './pages/Login';
import Inventory from './pages/Inventory';
import Inbound from './pages/Inbound';
import Outbound from './pages/Outbound';
import UploadCSV from './pages/UploadCSV';
import Navbar from './components/Navbar';


function App() {
  const isAuthenticated = !!localStorage.getItem('access_token');

  return (
    <Router>
      {isAuthenticated && <Navbar />}
      <Routes>
        <Route path="/upload" element={<UploadCSV />} />
        <Route path="/login" element={<Login />} />
        <Route path="/inventory" element={<Inventory />} />
        <Route path="/inbound" element={<Inbound />} />
        <Route path="/outbound" element={<Outbound />} />
      </Routes>
    </Router>
  );
}

export default App;

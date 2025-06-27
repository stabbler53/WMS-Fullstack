// App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Inventory from './pages/Inventory';
import Inbound from './pages/Inbound';
import Outbound from './pages/Outbound';
import UploadCSV from './pages/UploadCSV';
import Dashboard from './pages/Dashboard';
import ProtectedRoute from './components/ProtectedRoute';
import RequireAdmin from './components/RequireAdmin'; // ✅ import admin guard
import MainLayout from './layouts/MainLayout';

function App() {
  const isLoggedIn = !!localStorage.getItem('access_token');

  return (
    <Router>
      {isLoggedIn && <Navbar />}
      <MainLayout>
        <Routes>
          <Route path="/login" element={<Login />} />

          {/* ✅ Protected Routes */}
          <Route
            path="/inventory"
            element={<ProtectedRoute><Inventory /></ProtectedRoute>}
          />
          <Route
            path="/inbound"
            element={<ProtectedRoute><Inbound /></ProtectedRoute>}
          />
          <Route
            path="/outbound"
            element={<ProtectedRoute><Outbound /></ProtectedRoute>}
          />

          {/* ✅ Admin-Only Routes */}
          <Route
            path="/upload"
            element={
              <ProtectedRoute>
                <RequireAdmin>
                  <UploadCSV />
                </RequireAdmin>
              </ProtectedRoute>
            }
          />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <RequireAdmin>
                  <Dashboard />
                </RequireAdmin>
              </ProtectedRoute>
            }
          />

          {/* Optional fallback */}
          <Route path="*" element={<Login />} />
        </Routes>
      </MainLayout>
    </Router>
  );
}

export default App;

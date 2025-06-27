import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import API from '../services/api';

function Navbar() {
  const [role, setRole] = useState('');
  const [menuOpen, setMenuOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    API.get('users/me/')
      .then(res => setRole(res.data.role))
      .catch(() => setRole(''));
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/login');
  };

  // Don't show navbar on login page
  if (location.pathname === '/login') {
    return null;
  }

  return (
    <nav className="bg-white shadow-md border-b border-gray-100 sticky top-0 z-50">
      <div className="max-w-5xl mx-auto px-4 py-2 flex items-center justify-between">
        {/* Logo and Brand */}
        <div className="flex items-center gap-2">
          <img src="/logo192.png" alt="WMS Logo" className="h-8 w-8" />
          <span className="font-bold text-xl text-blue-700 tracking-tight">WMS</span>
        </div>
        {/* Desktop Menu */}
        <div className="hidden md:flex gap-6 items-center font-medium">
          <Link to="/dashboard" className="hover:text-blue-600 transition">Dashboard</Link>
          <Link to="/inventory" className="hover:text-blue-600 transition">Inventory</Link>
          {role !== 'operator' && (
            <>
              <Link to="/inbound" className="hover:text-blue-600 transition">Inbound</Link>
              <Link to="/outbound" className="hover:text-blue-600 transition">Outbound</Link>
            </>
          )}
          {role === 'admin' && (
            <Link to="/upload" className="hover:text-blue-600 transition">Upload CSV</Link>
          )}
        </div>
        {/* Mobile Hamburger */}
        <div className="md:hidden flex items-center">
          <button
            onClick={() => setMenuOpen(!menuOpen)}
            className="focus:outline-none p-2 rounded hover:bg-blue-50"
            aria-label="Toggle menu"
          >
            <svg className="h-6 w-6 text-blue-700" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              {menuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8h16M4 16h16" />
              )}
            </svg>
          </button>
        </div>
        {/* Logout Button */}
        <button
          onClick={handleLogout}
          className="ml-4 text-red-500 hover:text-red-700 font-semibold px-3 py-1 rounded transition border border-red-100 bg-red-50 hidden md:block"
        >
          Logout
        </button>
      </div>
      {/* Mobile Menu Dropdown */}
      {menuOpen && (
        <div className="md:hidden bg-white border-t border-gray-100 shadow-lg animate-fade-in-down">
          <div className="flex flex-col gap-2 p-4 font-medium">
            <Link to="/dashboard" className="hover:text-blue-600 transition" onClick={() => setMenuOpen(false)}>Dashboard</Link>
            <Link to="/inventory" className="hover:text-blue-600 transition" onClick={() => setMenuOpen(false)}>Inventory</Link>
            {role !== 'operator' && (
              <>
                <Link to="/inbound" className="hover:text-blue-600 transition" onClick={() => setMenuOpen(false)}>Inbound</Link>
                <Link to="/outbound" className="hover:text-blue-600 transition" onClick={() => setMenuOpen(false)}>Outbound</Link>
              </>
            )}
            {role === 'admin' && (
              <Link to="/upload" className="hover:text-blue-600 transition" onClick={() => setMenuOpen(false)}>Upload CSV</Link>
            )}
            <button
              onClick={() => { setMenuOpen(false); handleLogout(); }}
              className="text-red-500 hover:text-red-700 font-semibold px-3 py-1 rounded transition border border-red-100 bg-red-50 mt-2"
            >
              Logout
            </button>
          </div>
        </div>
      )}
    </nav>
  );
}

export default Navbar;

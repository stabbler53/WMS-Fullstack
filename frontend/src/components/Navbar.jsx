import { Link, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import API from '../services/api';

function Navbar() {
  const [role, setRole] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    API.get('users/me/')
      .then(res => setRole(res.data.role))
      .catch(() => setRole(''));
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/login');
  };

  return (
    <nav className="bg-gray-800 text-white p-4 flex justify-between items-center shadow-md">
      {/* Left side: Navigation links */}
      <div className="flex gap-4 items-center">
        <Link to="/inventory" className="hover:underline">
          Inventory
        </Link>

        {role !== 'Operator' && (
          <>
            <Link to="/inbound" className="hover:underline">
              Inbound
            </Link>
            <Link to="/outbound" className="hover:underline">
              Outbound
            </Link>
          </>
        )}

        {role === 'Admin' && (
          <Link to="/upload-csv" className="hover:underline">
            Upload CSV
          </Link>
        )}
      </div>

      {/* Right side: Logout button */}
      <button
        onClick={handleLogout}
        className="text-red-400 hover:text-red-200 transition"
      >
        Logout
      </button>
    </nav>
  );
}

export default Navbar;

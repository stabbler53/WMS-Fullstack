import { Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { useEffect, useState } from 'react';
import API from '../services/api';

toast.success("Outbound logged!");
toast.error("Not enough stock!");

function Navbar() {
  const [role, setRole] = useState('');

  useEffect(() => {
    API.get('users/me/')
      .then(res => setRole(res.data.role)) // Assuming backend has a `me` endpoint returning role
      .catch(() => setRole(''));
  }, []);

  return (
    <nav className="bg-gray-800 text-white p-4 flex gap-4">
      <Link to="/inventory">Inventory</Link>
      {role !== 'Operator' && <Link to="/inbound">Inbound</Link>}
      {role !== 'Operator' && <Link to="/outbound">Outbound</Link>}
      {role === 'Admin' && <Link to="/upload">Upload CSV</Link>}
      <button onClick={() => {
        localStorage.removeItem('access_token');
        window.location.href = '/login';
      }}>Logout</button>
    </nav>
  );
}

export default Navbar;

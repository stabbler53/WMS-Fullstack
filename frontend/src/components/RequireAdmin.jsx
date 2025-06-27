// components/RequireAdmin.jsx
import { useEffect, useRef, useState } from 'react';
import { Navigate } from 'react-router-dom';
import API from '../services/api';
import toast from 'react-hot-toast';
import Spinner from './Spinner'; // Optional: use your custom spinner component

function RequireAdmin({ children }) {
  const [role, setRole] = useState(null);
  const [loading, setLoading] = useState(true);
  const toastShown = useRef(false); // ✅ Prevents toast showing multiple times

  useEffect(() => {
    const fetchRole = async () => {
      try {
        const res = await API.get('users/me/');
        setRole(res.data.role);
      } catch {
        setRole(null);
      } finally {
        setLoading(false);
      }
    };

    fetchRole();
  }, []);

  if (loading) {
    return <Spinner message="Checking admin access..." />; // Or fallback text
  }

  if (role !== 'admin') {
    if (!toastShown.current) {
      toast.error('Access denied: Admins only');
      toastShown.current = true;
    }
    return <Navigate to="/inventory" replace />;
  }

  return children;
}

export default RequireAdmin;

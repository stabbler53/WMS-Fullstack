// src/components/ProtectedRoute.jsx
import { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import API from '../services/api';
import Spinner from './Spinner';

function ProtectedRoute({ children, allowedRoles }) {
  const [loading, setLoading] = useState(true);
  const [isAllowed, setIsAllowed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('access_token');

      if (!token) {
        navigate('/login', { state: { from: location } });
        return;
      }

      try {
        const res = await API.get('users/me/');
        const userRole = res.data.role;

        if (!allowedRoles || allowedRoles.includes(userRole)) {
          setIsAllowed(true);
        } else {
          navigate('/inventory');
        }
      } catch (err) {
        console.error(err);
        navigate('/login');
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, [allowedRoles, navigate, location]);

  if (loading) return <Spinner message="Checking access..." />;
  return isAllowed ? children : null;
}

export default ProtectedRoute;

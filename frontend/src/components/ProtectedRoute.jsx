import React, { useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import axios from 'axios';

const ProtectedRoute = ({ children, allowedRoles }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    const fetchUser = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        setError(true);
        setLoading(false);
        return;
      }

      try {
        axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        const res = await axios.get('/api/v1/protected/auth/me');
        setUser(res.data);
      } catch (err) {
        localStorage.removeItem('token');
        setError(true);
      } finally {
        setLoading(false);
      }
    };
    fetchUser();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-slate-800"></div>
      </div>
    );
  }

  if (error || !user) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    // Redirect based on their actual role if they try to access forbidden route
    if (user.role === 'admin') return <Navigate to="/admin" replace />;
    if (user.role === 'instructor') return <Navigate to="/instructor" replace />;
    return <Navigate to="/dashboard" replace />;
  }

  // Pass user object down to children using React.cloneElement
  return React.cloneElement(children, { user });
};

export default ProtectedRoute;

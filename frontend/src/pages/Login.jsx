import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { BookOpen, Lock, User, Loader2 } from 'lucide-react';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('/api/v1/auth/sign-in', {
        username,
        password
      });

      if (response.data.access) {
        localStorage.setItem('token', response.data.access);
        navigate('/dashboard');
      }
    } catch (err) {
      setError('Login gagal. Periksa kembali username dan password Anda.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-apple-bg px-4">
      <div className="bg-white/80 backdrop-blur-xl p-10 rounded-[32px] shadow-apple w-full max-w-md border border-white">
        <div className="flex flex-col items-center mb-10">
          <div className="bg-apple-blue p-3.5 rounded-2xl mb-5 shadow-sm">
            <BookOpen className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold tracking-tight text-apple-dark">Simple LMS</h1>
          <p className="text-apple-gray mt-2 text-center text-sm font-medium">Masuk ke portal pembelajaran Anda</p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-100/80 border-l-4 border-red-500 text-red-700 rounded-r shadow-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleLogin} className="space-y-6">
          <div className="space-y-2">
            <label className="text-sm font-semibold text-gray-600">Username</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <User className="h-5 w-5 text-gray-400" />
              </div>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full pl-11 pr-4 py-3.5 rounded-2xl border-0 focus:outline-none focus:ring-2 focus:ring-apple-blue transition-all bg-[#F0F0F2] text-apple-dark"
                placeholder="Masukkan username"
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-apple-gray ml-1">Password</label>
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                <Lock className="h-5 w-5 text-apple-gray/70" />
              </div>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full pl-11 pr-4 py-3.5 rounded-2xl border-0 focus:outline-none focus:ring-2 focus:ring-apple-blue transition-all bg-[#F0F0F2] text-apple-dark"
                placeholder="Masukkan password"
                required
              />
            </div>
          </div>

          <div className="pt-2">
            <button
              type="submit"
              disabled={loading}
              className="w-full py-3.5 px-4 bg-apple-blue hover:bg-apple-blue-hover text-white font-semibold rounded-full transition-colors flex items-center justify-center"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : 'Masuk Sekarang'}
            </button>
          </div>
        </form>

        <div className="mt-8 pt-6 border-t border-black/5">
          <div className="bg-black/5 p-4 rounded-2xl text-sm text-apple-gray flex flex-col items-center">
            <p className="font-semibold text-apple-dark mb-2">Demo Akun (Student):</p>
            <div className="flex space-x-4">
              <p>User: <code className="bg-white px-2 py-1 rounded-lg text-apple-blue shadow-sm">student</code></p>
              <p>Pass: <code className="bg-white px-2 py-1 rounded-lg text-apple-blue shadow-sm">123</code></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;

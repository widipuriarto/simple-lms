import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { Users, ChevronLeft, Shield, User, Search } from 'lucide-react';

export default function AdminUsers() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const res = await axios.get('/api/v1/protected/admin/users');
        setUsers(res.data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchUsers();
  }, []);

  const filteredUsers = users.filter(u => 
    u.username.toLowerCase().includes(searchTerm.toLowerCase()) || 
    u.email.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (loading) {
    return (
      <div className="flex justify-center items-center py-40">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-apple-blue"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6 animate-fade-in max-w-6xl mx-auto pb-12">
      <Link to="/admin" className="inline-flex items-center text-sm font-semibold text-apple-gray hover:text-apple-dark transition-colors mb-2">
        <ChevronLeft className="w-4 h-4 mr-1" /> Kembali ke Analytics
      </Link>
      
      <div className="bg-white/70 backdrop-blur-xl p-8 rounded-[32px] shadow-apple border border-white flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div className="flex items-center space-x-4">
          <div className="bg-blue-50 p-4 rounded-2xl text-apple-blue">
            <Users className="w-8 h-8" />
          </div>
          <div>
            <h1 className="text-3xl font-bold text-apple-dark mb-1">Daftar Pengguna</h1>
            <p className="text-apple-gray font-medium">Kelola seluruh Student dan Instructor di platform.</p>
          </div>
        </div>
        
        <div className="relative w-full md:w-72">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            className="w-full pl-10 pr-4 py-3 rounded-2xl border-0 focus:ring-2 focus:ring-apple-blue bg-[#F0F0F2] text-apple-dark transition-all"
            placeholder="Cari pengguna..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      <div className="bg-white/80 backdrop-blur-xl rounded-[32px] shadow-apple border border-white overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gray-50/50 border-b border-gray-100">
                <th className="px-6 py-5 text-sm font-semibold text-gray-500 uppercase tracking-wider">ID</th>
                <th className="px-6 py-5 text-sm font-semibold text-gray-500 uppercase tracking-wider">Username</th>
                <th className="px-6 py-5 text-sm font-semibold text-gray-500 uppercase tracking-wider">Email</th>
                <th className="px-6 py-5 text-sm font-semibold text-gray-500 uppercase tracking-wider">Role</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {filteredUsers.map(user => (
                <tr key={user.id} className="hover:bg-gray-50/50 transition-colors">
                  <td className="px-6 py-5 text-sm font-medium text-gray-900">#{user.id}</td>
                  <td className="px-6 py-5 text-sm font-semibold text-apple-dark flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-500">
                      <User className="w-4 h-4" />
                    </div>
                    {user.username}
                  </td>
                  <td className="px-6 py-5 text-sm text-gray-500">{user.email || '-'}</td>
                  <td className="px-6 py-5">
                    <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${
                      user.role === 'admin' ? 'bg-purple-100 text-purple-700' :
                      user.role === 'instructor' ? 'bg-orange-100 text-orange-700' :
                      'bg-blue-100 text-blue-700'
                    }`}>
                      {user.role === 'admin' && <Shield className="w-3 h-3 mr-1" />}
                      {user.role}
                    </span>
                  </td>
                </tr>
              ))}
              {filteredUsers.length === 0 && (
                <tr>
                  <td colSpan="4" className="px-6 py-10 text-center text-gray-500">
                    Tidak ada pengguna yang ditemukan.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
